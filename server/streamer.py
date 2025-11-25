import math
import logging
import asyncio
from pyrogram import Client, utils
from pyrogram.file_id import FileId
from pyrogram.raw.functions.upload import GetFile
from pyrogram.raw.types import InputFileLocation
from pyrogram.errors import FileMigrate, FloodWait
from collections import defaultdict
import os

# Global registry: DC ID → Client
dc_clients = {}
dc_locks = defaultdict(asyncio.Lock)

# Global mapping: file_id → DC ID (so we know which DC each file belongs to)
file_dc_mapping = {}

class TelegramFileStreamer:
    def __init__(self, client: Client, file_id: str, file_size: int):
        self.client = client
        self.file_id = file_id
        self.file_size = file_size
        self.chunk_size = 512 * 1024  # 512 KiB chunks to avoid LIMIT_INVALID errors
        
        # Determine which client to use based on file_id mapping
        if file_id in file_dc_mapping:
            # We already know which DC this file is on
            target_dc = file_dc_mapping[file_id]
            self.download_client = dc_clients.get(target_dc, client)
            logging.info(f"Using cached DC {target_dc} client for file {file_id[:20]}...")
        else:
            # First time seeing this file, use default client
            self.download_client = client
        
        self.is_temp_client = False
        self.cached_location = None

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
            # Get file location (use cached if available)
            if self.cached_location is None:
                try:
                    self.cached_location = await self.get_file_location()
                except Exception as e:
                    logging.error(f"Failed to get file location: {e}")
                    raise e
            
            location = self.cached_location

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
                    result = await self.download_client.invoke(
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
                    target_dc = e.value
                    logging.warning(f"DC Migration: File is on DC {target_dc}")
                    
                    # Use a lock to ensure we only create/start the client once per DC
                    async with dc_locks[target_dc]:
                        if target_dc in dc_clients:
                            logging.info(f"Reusing existing DC {target_dc} client")
                            self.download_client = dc_clients[target_dc]
                        else:
                            logging.info(f"Creating new client for DC {target_dc}...")
                            
                            # Use a stable session name to reuse auth (avoids FloodWait)
                            session_name = f"persistent_dc_{target_dc}"
                            
                            # Use persistent directory for sessions
                            from bot_client import SESSION_DIR
                            from config import Config
                            new_client = Client(
                                session_name,
                                api_id=Config.API_ID,
                                api_hash=Config.API_HASH,
                                bot_token=Config.BOT_TOKEN,
                                workdir=SESSION_DIR,
                                no_updates=True
                            )
                            
                            # If session file doesn't exist, we must set the DC ID first
                            session_path = os.path.join(SESSION_DIR, f"{session_name}.session")
                            if not os.path.exists(session_path):
                                logging.info(f"Setting DC ID {target_dc} for new session...")
                                await new_client.storage.open()
                                await new_client.storage.dc_id(target_dc)
                                await new_client.storage.save()
                                await new_client.storage.close()
                            
                            logging.info(f"Starting client for DC {target_dc}...")
                            try:
                                await new_client.start()
                                dc_clients[target_dc] = new_client
                                self.download_client = new_client
                                logging.info(f"DC {target_dc} client started and cached.")
                            except FloodWait as flood_err:
                                # Handle FloodWait gracefully - wait it out and retry
                                wait_time = flood_err.value
                                logging.warning(f"⚠️ FloodWait: Need to wait {wait_time} seconds before creating DC {target_dc} client")
                                logging.info(f"Waiting {wait_time}s... (This is due to recent repeated deployments)")
                                await asyncio.sleep(wait_time)
                                logging.info(f"FloodWait over. Retrying DC {target_dc} client creation...")
                                # Retry after waiting
                                await new_client.start()
                                dc_clients[target_dc] = new_client
                                self.download_client = new_client
                                logging.info(f"DC {target_dc} client started and cached after FloodWait.")
                            except Exception as client_err:
                                logging.error(f"Failed to start DC {target_dc} client: {client_err}")
                                raise client_err
                    
                    # IMPORTANT: Save the mapping so future requests use the correct DC immediately
                    file_dc_mapping[self.file_id] = target_dc
                    logging.info(f"Saved mapping: file {self.file_id[:20]}... → DC {target_dc}")

                    # Refresh location for the new DC and update cache
                    self.cached_location = await self.get_file_location()
                    location = self.cached_location
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
