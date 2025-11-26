"""
ByteStreamer - Advanced file streaming with caching and session management
Inspired by: https://github.com/eyaadh/megadlbot_oss
"""
import math
import asyncio
import logging
from typing import Dict, Union, AsyncGenerator
from pyrogram import Client
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from pyrogram.session import Session, Auth
from pyrogram.errors import AuthBytesInvalid, FileMigrate, FloodWait
from pyrogram import raw, utils

logger = logging.getLogger(__name__)


class ByteStreamer:
    """
    A custom class that holds the cache of a specific client and streaming functions.
    
    Attributes:
        client: The Pyrogram client instance
        cached_file_ids: Dict of cached file IDs and their properties
        clean_timer: Cache cleanup interval in seconds (default: 30 minutes)
    
    Functions:
        get_file_properties: Returns cached or fetches file properties
        generate_media_session: Creates/returns media session for specific DC
        get_location: Returns InputFileLocation for the file
        yield_file: Yields file chunks for streaming
        clean_cache: Periodically cleans the cache
    """

    def __init__(self, client: Client):
        """Initialize ByteStreamer with a client."""
        self.clean_timer = 30 * 60  # 30 minutes
        self.client: Client = client
        self.cached_file_ids: Dict[int, FileId] = {}
        asyncio.create_task(self.clean_cache())
        logger.info("ByteStreamer initialized")

    async def get_file_properties(self, chat_id: int, message_id: int) -> FileId:
        """
        Returns the properties of a media file in a FileId class.
        If cached, returns cached results. Otherwise, fetches and caches.
        
        Args:
            chat_id: Telegram chat ID
            message_id: Telegram message ID
            
        Returns:
            FileId: File properties
        """
        cache_key = f"{chat_id}:{message_id}"
        
        if cache_key not in self.cached_file_ids:
            await self.generate_file_properties(chat_id, message_id)
            logger.debug(f"Cached file properties for {cache_key}")
        
        return self.cached_file_ids[cache_key]

    async def generate_file_properties(self, chat_id: int, message_id: int) -> FileId:
        """
        Generates and caches the properties of a media file.
        
        Args:
            chat_id: Telegram chat ID
            message_id: Telegram message ID
            
        Returns:
            FileId: File properties
        """
        try:
            msg = await self.client.get_messages(chat_id, message_id)
            
            if not msg or not msg.media:
                raise ValueError(f"No media found in message {message_id}")
            
            media = getattr(msg, msg.media.value)
            file_id = FileId.decode(media.file_id)
            
            cache_key = f"{chat_id}:{message_id}"
            self.cached_file_ids[cache_key] = file_id
            
            logger.debug(f"Generated file ID for {cache_key}")
            return file_id
            
        except Exception as e:
            logger.error(f"Failed to generate file properties: {e}")
            raise

    async def generate_media_session(self, client: Client, file_id: FileId) -> Session:
        """
        Generates or returns cached media session for the DC containing the file.
        This is required for getting bytes from Telegram servers.
        
        Args:
            client: Pyrogram client
            file_id: Decoded file ID
            
        Returns:
            Session: Media session for the file's DC
        """
        media_session = client.media_sessions.get(file_id.dc_id, None)

        if media_session is None:
            if file_id.dc_id != await client.storage.dc_id():
                # File is on a different DC, need to create session
                media_session = Session(
                    client,
                    file_id.dc_id,
                    await Auth(
                        client, file_id.dc_id, await client.storage.test_mode()
                    ).create(),
                    await client.storage.test_mode(),
                    is_media=True,
                )
                await media_session.start()

                # Export and import authorization
                for attempt in range(6):
                    try:
                        exported_auth = await client.invoke(
                            raw.functions.auth.ExportAuthorization(dc_id=file_id.dc_id)
                        )
                        
                        await media_session.send(
                            raw.functions.auth.ImportAuthorization(
                                id=exported_auth.id, bytes=exported_auth.bytes
                            )
                        )
                        break
                    except AuthBytesInvalid:
                        logger.debug(f"Invalid auth bytes for DC {file_id.dc_id}, attempt {attempt + 1}")
                        if attempt == 5:
                            await media_session.stop()
                            raise
                        continue
            else:
                # File is on same DC as client
                media_session = Session(
                    client,
                    file_id.dc_id,
                    await client.storage.auth_key(),
                    await client.storage.test_mode(),
                    is_media=True,
                )
                await media_session.start()
            
            logger.debug(f"Created media session for DC {file_id.dc_id}")
            client.media_sessions[file_id.dc_id] = media_session
        else:
            logger.debug(f"Using cached media session for DC {file_id.dc_id}")
        
        return media_session

    @staticmethod
    async def get_location(file_id: FileId) -> Union[
        raw.types.InputPhotoFileLocation,
        raw.types.InputDocumentFileLocation,
        raw.types.InputPeerPhotoFileLocation,
    ]:
        """
        Returns the InputFileLocation for the media file.
        
        Args:
            file_id: Decoded file ID
            
        Returns:
            InputFileLocation: Location object for the file
        """
        file_type = file_id.file_type

        if file_type == FileType.CHAT_PHOTO:
            if file_id.chat_id > 0:
                peer = raw.types.InputPeerUser(
                    user_id=file_id.chat_id, access_hash=file_id.chat_access_hash
                )
            else:
                if file_id.chat_access_hash == 0:
                    peer = raw.types.InputPeerChat(chat_id=-file_id.chat_id)
                else:
                    peer = raw.types.InputPeerChannel(
                        channel_id=utils.get_channel_id(file_id.chat_id),
                        access_hash=file_id.chat_access_hash,
                    )

            location = raw.types.InputPeerPhotoFileLocation(
                peer=peer,
                volume_id=file_id.volume_id,
                local_id=file_id.local_id,
                big=file_id.thumbnail_source == ThumbnailSource.CHAT_PHOTO_BIG,
            )
        elif file_type == FileType.PHOTO:
            location = raw.types.InputPhotoFileLocation(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
                thumb_size=file_id.thumbnail_size,
            )
        else:
            # Document, Video, Audio, etc.
            location = raw.types.InputDocumentFileLocation(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
                thumb_size=file_id.thumbnail_size,
            )
        
        return location

    async def yield_file(
        self,
        file_id: FileId,
        offset: int,
        first_part_cut: int,
        last_part_cut: int,
        part_count: int,
        chunk_size: int,
    ) -> AsyncGenerator[bytes, None]:
        """
        Custom generator that yields the bytes of the media file.
        
        Args:
            file_id: Decoded file ID
            offset: Starting byte offset
            first_part_cut: Bytes to skip in first chunk
            last_part_cut: Bytes to keep in last chunk
            part_count: Number of chunks to fetch
            chunk_size: Size of each chunk
            
        Yields:
            bytes: File chunks
        """
        client = self.client
        current_part = 1
        
        logger.debug(f"Starting to yield file with {part_count} parts")
        
        media_session = await self.generate_media_session(client, file_id)
        location = await self.get_location(file_id)

        try:
            r = await media_session.send(
                raw.functions.upload.GetFile(
                    location=location, offset=offset, limit=chunk_size
                ),
            )
            
            if isinstance(r, raw.types.upload.File):
                while True:
                    chunk = r.bytes
                    if not chunk:
                        break
                    
                    # Handle first/last part cutting for precise range requests
                    if part_count == 1:
                        yield chunk[first_part_cut:last_part_cut]
                    elif current_part == 1:
                        yield chunk[first_part_cut:]
                    elif current_part == part_count:
                        yield chunk[:last_part_cut]
                    else:
                        yield chunk

                    current_part += 1
                    offset += chunk_size

                    if current_part > part_count:
                        break

                    r = await media_session.send(
                        raw.functions.upload.GetFile(
                            location=location, offset=offset, limit=chunk_size
                        ),
                    )
        except (TimeoutError, AttributeError) as e:
            logger.error(f"Error while yielding file: {e}")
        except FloodWait as e:
            logger.warning(f"FloodWait during file yield: {e.value}s")
            await asyncio.sleep(e.value)
        except Exception as e:
            logger.exception(f"Unexpected error during file yield: {e}")
        finally:
            logger.debug(f"Finished yielding file with {current_part - 1} parts")

    async def clean_cache(self) -> None:
        """
        Periodically cleans the cache to reduce memory usage.
        Runs every 30 minutes by default.
        """
        while True:
            await asyncio.sleep(self.clean_timer)
            self.cached_file_ids.clear()
            logger.debug("Cleaned file cache")
