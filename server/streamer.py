import math
import logging
import asyncio
from pyrogram import Client, utils
from pyrogram.file_id import FileId
from pyrogram.raw.functions.upload import GetFile
from pyrogram.raw.types import InputFileLocation
from pyrogram.errors import FileMigrate, FloodWait

class TelegramFileStreamer:
    def __init__(self, client: Client, file_id: str, file_size: int):
        self.client = client
        self.file_id = file_id
        self.file_size = file_size
        self.chunk_size = 512 * 1024  # 512 KiB chunks to avoid LIMIT_INVALID errors

    async def get_file_location(self):
        # Decode the file_id to get the location
        decoded = FileId.decode(self.file_id)
        
        # Create InputFileLocation manually from decoded FileId
        from pyrogram.raw.types import InputDocumentFileLocation, InputPhotoFileLocation
        
        # Check the file type and create appropriate location
        if decoded.file_type in [1, 2]:  # Photo
            media_input_location = InputPhotoFileLocation(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
                thumb_size=""
            )
        else:  # Document, Video, Audio, etc.
            media_input_location = InputDocumentFileLocation(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
                thumb_size=""
            )
        
        return media_input_location

    async def yield_chunks(self, start: int, end: int):
        # Stream file chunks using direct GetFile calls.
        # Handles DC migration by retrying requests.
        # Supports random access for fast seeking.

        # Telegram requires offset to be divisible by 4096 (4KB)
        current_offset = start

        while current_offset < end:
            # Always get a fresh location (covers any DC migration)
            location = await self.get_file_location()

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
            # Cap request size to chunk_size (now 512 KiB)
            if request_limit > self.chunk_size:
                request_limit = self.chunk_size

            retries = 5
            while retries > 0:
                try:
                    result = await self.client.invoke(
                        GetFile(
                            location=location,
                            offset=aligned_offset,
                            limit=request_limit,
                        )
                    )
                    chunk = result.bytes

                    if gap:
                        chunk = chunk[gap:]
                    if len(chunk) > bytes_needed:
                        chunk = chunk[:bytes_needed]

                    if not chunk:
                        return

                    yield chunk
                    current_offset += len(chunk)
                    break  # success

                except FileMigrate as e:
                    logging.warning(
                        f"DC Migration detected (DC {e.value}). Updating client DC and retrying..."
                    )
                    # Update client session DC if possible
                    try:
                        # Change the client's DC settings and reconnect
                        self.client.session.dc_id = e.value

                        # Stop the current session
                        await self.client.session.stop()

                        # If we have access to the actual API instance, update it
                        if hasattr(self.client, 'storage'):
                            # Reinitialize the connection for the new DC
                            await self.client.connect()
                    except Exception as sess_err:
                        logging.error(f"Failed to handle DC migration: {sess_err}")

                    # Wait a bit before retrying
                    await asyncio.sleep(1)
                    # Refresh location for the new DC
                    location = await self.get_file_location()
                    retries -= 1
                    if retries > 0:
                        await asyncio.sleep(2)  # Wait longer between retries for DC migration
                    continue

                except FloodWait as e:
                    logging.warning(f"FloodWait: sleeping {e.value}s")
                    await asyncio.sleep(e.value)
                    continue

                except Exception as exc:
                    logging.error(f"GetFile error at offset {current_offset}: {exc}")
                    retries -= 1
                    await asyncio.sleep(1)
                    if retries == 0:
                        raise exc
