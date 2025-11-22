import math
import logging
import asyncio
import os
import tempfile
from pyrogram import Client
from pyrogram.file_id import FileId

class TelegramFileStreamer:
    def __init__(self, client: Client, file_id: str, file_size: int):
        self.client = client
        self.file_id = file_id
        self.file_size = file_size
        self.chunk_size = 1024 * 1024 # 1MB chunks

    async def get_file_location(self):
        # Kept for compatibility, not used in new logic
        return None

    async def yield_chunks(self, start: int, end: int):
        """
        Streams the file by downloading it to a temp file in the background
        and yielding bytes as they become available.
        """
        # Create a temp file
        fd, temp_path = tempfile.mkstemp()
        os.close(fd)
        
        download_task = None
        
        try:
            # Start download in background
            # We use a specific file name so Pyrogram writes to it
            download_task = asyncio.create_task(
                self.client.download_media(self.file_id, file_name=temp_path)
            )
            
            # Loop until we have served the requested range
            current = start
            last_log_time = 0
            while current < end:
                # Check current file size
                if os.path.exists(temp_path):
                    file_size_on_disk = os.path.getsize(temp_path)
                else:
                    file_size_on_disk = 0

                # Log status every 2 seconds to avoid spam
                import time
                if time.time() - last_log_time > 2:
                    logging.info(f"Stream status: current={current}, on_disk={file_size_on_disk}, target={end}")
                    last_log_time = time.time()

                # If we have data to read
                if file_size_on_disk > current:
                    # Calculate how much we can read
                    # We can read up to 'end' or up to what's available on disk
                    available = file_size_on_disk - current
                    to_read = min(self.chunk_size, available, end - current)
                    
                    if to_read > 0:
                        with open(temp_path, "rb") as f:
                            f.seek(current)
                            chunk = f.read(to_read)
                            if chunk:
                                # logging.debug(f"Yielding chunk: {len(chunk)} bytes")
                                yield chunk
                                current += len(chunk)
                                continue

                # Check if download finished or failed
                if download_task.done():
                    try:
                        result = download_task.result() # Raise exception if failed
                        logging.info(f"Download task finished. Result: {result}")
                        # If finished and we haven't reached 'end' yet, but file is fully read
                        if file_size_on_disk <= current:
                            logging.info("Download finished but no more data to read. Ending stream.")
                            break # End of file
                    except Exception as e:
                        logging.error(f"Background download failed: {e}")
                        raise e
                
                # Wait for more data
                await asyncio.sleep(0.1)

        except Exception as e:
            logging.error(f"Streaming error: {e}")
            raise
        finally:
            # Cleanup
            if download_task and not download_task.done():
                download_task.cancel()
                try:
                    await download_task
                except asyncio.CancelledError:
                    pass
            
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
