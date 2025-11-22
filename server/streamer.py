import math
import logging
import asyncio
from pyrogram import Client, utils
from pyrogram.file_id import FileId
from pyrogram.raw.functions.upload import GetFile
from pyrogram.raw.types import InputFileLocation

class TelegramFileStreamer:
    def __init__(self, client: Client, file_id: str, file_size: int):
        self.client = client
        self.file_id = file_id
        self.file_size = file_size
        self.chunk_size = 1024 * 1024 # 1MB chunks

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
        """Yield file chunks using Pyrogram's download_media which handles DC migration.
        This loads the entire file into memory (acceptable for moderate file sizes) and then
        yields the requested byte range in 1MB chunks.
        """
        try:
            # Download the full file into memory as bytes
            full_bytes = await self.client.download_media(self.file_id, in_memory=True)
        except Exception as e:
            logging.error(f"Failed to download file {self.file_id}: {e}")
            raise e

        # Validate start/end
        file_len = len(full_bytes)
        if start < 0:
            start = 0
        if end <= 0 or end > file_len:
            end = file_len

        current = start
        while current < end:
            next_offset = min(current + self.chunk_size, end)
            chunk = full_bytes[current:next_offset]
            if not chunk:
                break
            yield chunk
            current = next_offset
