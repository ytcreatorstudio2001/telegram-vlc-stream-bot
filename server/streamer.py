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
        # Handles DC migration by retrying requests with a new client connected to the correct DC.
        
        from config import Config
        from pyrogram import Client
        
        # We start with the main client
        download_client = self.client
        is_temp_client = False

        # Telegram requires offset to be divisible by 4096 (4KB)
        current_offset = start

        try:
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
                # Cap request size to chunk_size
                if request_limit > self.chunk_size:
                    request_limit = self.chunk_size

                retries = 5
                while retries > 0:
                    try:
                        result = await download_client.invoke(
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
                        logging.warning(f"DC Migration detected (DC {e.value}). Switching to temporary client...")
                        
                        # If we already have a temp client, stop it first
                        if is_temp_client:
                            await download_client.stop()
                        
                        # Create a new temporary client for this DC
                        # We use a unique session name to avoid conflicts
                        import time
                        session_name = f"temp_dc_{e.value}_{int(time.time())}"
                        
                        new_client = Client(
                            session_name,
                            api_id=Config.API_ID,
                            api_hash=Config.API_HASH,
                            bot_token=Config.BOT_TOKEN,
                            in_memory=True,
                            no_updates=True
                        )
                        
                        # Force the new client to connect to the target DC
                        # We must set the DC ID in storage before starting
                        await new_client.storage.dc_id(e.value)
                        
                        logging.info(f"DEBUG: Starting temp client on DC {e.value}...")
                        await new_client.start()
                        logging.info("DEBUG: Temp client started and authenticated.")
                        
                        # Switch to the new client
                        download_client = new_client
                        is_temp_client = True
                        
                        # Refresh location for the new DC (although it should be the same)
                        # location = await self.get_file_location() 
                        # Actually, we might need to re-decode if the access_hash depends on context, 
                        # but usually the location object is static.
                        
                        retries -= 1
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
        finally:
            # Cleanup temp client if used
            if is_temp_client:
                logging.info("DEBUG: Stopping temporary download client...")
                try:
                    await download_client.stop()
                except Exception as e:
                    logging.error(f"Error stopping temp client: {e}")
