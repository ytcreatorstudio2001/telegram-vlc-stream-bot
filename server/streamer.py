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
        location = await self.get_file_location()
        
        # Telegram requires offset to be divisible by 4096 (4KB)
        current_offset = start
        
        while current_offset < end:
            aligned_offset = (current_offset // 4096) * 4096
            gap = current_offset - aligned_offset
            
            bytes_needed = min(self.chunk_size, end - current_offset)
            request_amount = gap + bytes_needed
            
            # Align request limit to 4096
            if request_amount % 4096 != 0:
                request_limit = math.ceil(request_amount / 4096) * 4096
            else:
                request_limit = request_amount
            
            # Safety cap 1MB + alignment
            if request_limit > 1024 * 1024 * 2:
                request_limit = 1024 * 1024 * 2

            retries = 3
            while retries > 0:
                try:
                    result = await self.client.invoke(
                        GetFile(
                            location=location,
                            offset=aligned_offset,
                            limit=request_limit
                        )
                    )
                    
                    chunk = result.bytes
                    
                    if gap > 0:
                        chunk = chunk[gap:]
                    
                    if len(chunk) > bytes_needed:
                        chunk = chunk[:bytes_needed]
                    
                    if not chunk:
                        # End of file reached unexpectedly
                        return

                    yield chunk
                    current_offset += len(chunk)
                    break # Success, exit retry loop
                    
                except Exception as e:
                    retries -= 1
                    logging.warning(f"Fetch error at {current_offset}: {e}. Retrying ({retries} left)...")
                    if retries == 0:
                        logging.error(f"Failed to fetch chunk at {current_offset} after retries.")
                        raise e
                    # Small delay before retry
                    await asyncio.sleep(1)
