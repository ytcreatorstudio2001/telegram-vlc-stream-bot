"""
Telegram File Streamer - Handles streaming files from Telegram with DC migration support
"""
import math
import logging
import asyncio
from pyrogram import Client
from pyrogram.file_id import FileId
from pyrogram.raw.functions.upload import GetFile
from pyrogram.raw.types import InputDocumentFileLocation, InputPhotoFileLocation
from pyrogram.errors import FileMigrate, FloodWait

from server.dc_manager import get_main_client, get_dc_client
from server.dc_mapping import get_file_dc, set_file_dc

logger = logging.getLogger(__name__)


class TelegramFileStreamer:
    """
    Streams Telegram files with intelligent DC routing and migration handling.
    """
    
    def __init__(self, chat_id: int, message_id: int, file_id: str, file_size: int):
        """
        Initialize the streamer.
        
        Args:
            chat_id: Telegram chat ID
            message_id: Telegram message ID
            file_id: Telegram file ID
            file_size: Total file size in bytes
        """
        self.chat_id = chat_id
        self.message_id = message_id
        self.file_id = file_id
        self.file_size = file_size
        self.chunk_size = 512 * 1024  # 512 KiB chunks
        self.client = None
        self.cached_location = None

    async def _ensure_client(self):
        """
        Ensure we have the correct client for this file.
        Uses DC mapping if available, otherwise uses main client.
        """
        if self.client is not None:
            return
            
        # Try to get DC from mapping
        dc_id = get_file_dc(self.chat_id, self.message_id)
        
        if dc_id is not None:
            try:
                self.client = await get_dc_client(dc_id)
                logger.info(f"Using cached DC {dc_id} client for Chat {self.chat_id}, Message {self.message_id}")
            except RuntimeError as e:
                # FloodWait or client creation failed
                logger.error(f"Failed to get DC {dc_id} client: {e}")
                # Fall back to main client
                self.client = await get_main_client()
        else:
            # First time seeing this file, use main client
            self.client = await get_main_client()

    async def get_file_location(self):
        """
        Decode file_id and create InputFileLocation.
        
        Returns:
            InputFileLocation for the file
        """
        decoded = FileId.decode(self.file_id)
        
        # Create appropriate location based on file type
        if decoded.file_type in [1, 2]:  # Photo
            return InputPhotoFileLocation(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
                thumb_size=""
            )
        else:  # Document, Video, Audio, etc.
            return InputDocumentFileLocation(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
                thumb_size=""
            )

    async def yield_chunks(self, start: int = 0, end: int = None):
        """
        Stream file chunks with DC migration handling.
        
        Args:
            start: Starting byte offset
            end: Ending byte offset (None = end of file)
            
        Yields:
            bytes: File chunks
        """
        # Ensure we have a client
        await self._ensure_client()
        
        if end is None:
            end = self.file_size
            
        current_offset = start

        while current_offset < end:
            # Get file location (cache it after first fetch)
            if self.cached_location is None:
                try:
                    self.cached_location = await self.get_file_location()
                except Exception as e:
                    logger.error(f"Failed to get file location: {e}")
                    raise

            location = self.cached_location

            # Calculate aligned offset and chunk size
            aligned_offset = (current_offset // 4096) * 4096
            gap = current_offset - aligned_offset
            bytes_needed = min(self.chunk_size, end - current_offset)
            request_amount = gap + bytes_needed

            # Align request limit to 4096 bytes
            request_limit = (
                math.ceil(request_amount / 4096) * 4096
                if request_amount % 4096 != 0
                else request_amount
            )
            # Cap request size to chunk_size
            if request_limit > self.chunk_size:
                request_limit = self.chunk_size

            # Try to fetch the chunk
            try:
                result = await self.client.invoke(
                    GetFile(
                        location=location,
                        offset=aligned_offset,
                        limit=request_limit,
                    )
                )
                chunk = result.bytes

                # Trim chunk to requested range
                if gap:
                    chunk = chunk[gap:]
                if len(chunk) > bytes_needed:
                    chunk = chunk[:bytes_needed]

                if not chunk:
                    return  # EOF

                yield chunk
                current_offset += len(chunk)

            except FileMigrate as e:
                target_dc = e.value
                logger.warning(f"DC Migration: File is on DC {target_dc}")

                try:
                    new_client = await get_dc_client(target_dc)
                except RuntimeError as client_err:
                    # FloodWait or other DC client issue - stop streaming
                    logger.error(
                        f"Failed to get DC {target_dc} client for Chat {self.chat_id}, Message {self.message_id}: {client_err}"
                    )
                    return

                self.client = new_client
                
                # Save mapping for future requests
                set_file_dc(self.chat_id, self.message_id, target_dc)
                
                # Refresh location for the new DC
                self.cached_location = await self.get_file_location()
                
                # Retry once with the new client
                try:
                    result = await self.client.invoke(
                        GetFile(
                            location=self.cached_location,
                            offset=aligned_offset,
                            limit=request_limit,
                        )
                    )
                    chunk = result.bytes
                    
                    if gap:
                        chunk = chunk[gap:]
                    if len(chunk) > bytes_needed:
                        chunk = chunk[:bytes_needed]
                        
                    if chunk:
                        yield chunk
                        current_offset += len(chunk)
                        
                except FloodWait as fw:
                    logger.error(f"FloodWait while retrying on DC {target_dc}: {fw.value}s")
                    return
                except Exception as retry_err:
                    logger.exception(f"Retry after FileMigrate failed: {retry_err}")
                    return

            except FloodWait as e:
                logger.warning(f"FloodWait during streaming: {e.value}s")
                await asyncio.sleep(e.value)
                # Continue to retry

            except Exception as exc:
                logger.exception(f"GetFile error at offset {current_offset}: {exc}")
                return
