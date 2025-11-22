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
        """Yield file chunks from a temporary file.
        This avoids loading the whole file into memory and works with any file size.
        The file is downloaded once to a temp location, then read slice‑by‑slice.
        """
        import tempfile, os
        try:
            # Download the file to a temporary location (only once per request)
            temp_path = await self.client.download_media(self.file_id, file_name=None)
        except Exception as e:
            logging.error(f"Failed to download file {self.file_id}: {e}")
            raise e

        try:
            file_len = os.path.getsize(temp_path)
            # Adjust start/end bounds
            if start < 0:
                start = 0
            if end <= 0 or end > file_len:
                end = file_len

            with open(temp_path, "rb") as f:
                f.seek(start)
                current = start
                while current < end:
                    to_read = min(self.chunk_size, end - current)
                    chunk = f.read(to_read)
                    if not chunk:
                        break
                    yield chunk
                    current += len(chunk)
        finally:
            # Clean up the temporary file
            try:
                os.remove(temp_path)
            except Exception:
                pass
