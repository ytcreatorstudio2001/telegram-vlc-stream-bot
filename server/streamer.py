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
        return None

    async def yield_chunks(self, start: int, end: int):
        """
        Streams the file by downloading it to a temp file in the background.
        Crucially, it reads from the .temp file that Pyrogram creates while downloading.
        Includes logic to handle file renaming (temp -> final) and buffering.
        """
        # Create a temp file path (but don't create the file yet)
        fd, temp_path = tempfile.mkstemp()
        os.close(fd)
        os.remove(temp_path)
        
        download_task = None
        
        try:
            # Start download in background
            download_task = asyncio.create_task(
                self.client.download_media(self.file_id, file_name=temp_path)
            )
            
            current = start
            temp_file_path = temp_path + ".temp"
            final_file_path = temp_path
            
            # Buffer for small reads
            min_chunk_size = 64 * 1024 # 64KB
            
            while current < end:
                # Robust file finding loop
                active_path = None
                for _ in range(3): # Retry a few times in case of rename race
                    if os.path.exists(temp_file_path):
                        active_path = temp_file_path
                        break
                    elif os.path.exists(final_file_path):
                        active_path = final_file_path
                        break
                    await asyncio.sleep(0.1)
                
                if not active_path:
                    # If download task is done and no file found, something is wrong
                    if download_task.done():
                        # Check if it finished successfully just now
                        if os.path.exists(final_file_path):
                            active_path = final_file_path
                        else:
                             # Maybe failed?
                             try:
                                 download_task.result()
                             except Exception as e:
                                 raise e
                             break # File missing after success?
                    else:
                        # Wait for download to start creating file
                        await asyncio.sleep(0.5)
                        continue

                file_size_on_disk = 0
                try:
                    file_size_on_disk = os.path.getsize(active_path)
                except FileNotFoundError:
                    # Renamed while checking? Retry loop
                    continue

                # If we have data to read
                if file_size_on_disk > current:
                    available = file_size_on_disk - current
                    
                    # Wait for at least min_chunk_size unless download is done or we are near end
                    if available < min_chunk_size and not download_task.done() and (end - current) > min_chunk_size:
                        await asyncio.sleep(0.2)
                        continue

                    to_read = min(self.chunk_size, available, end - current)
                    
                    if to_read > 0:
                        try:
                            with open(active_path, "rb") as f:
                                f.seek(current)
                                chunk = f.read(to_read)
                                if chunk:
                                    yield chunk
                                    current += len(chunk)
                                    continue
                        except FileNotFoundError:
                            continue # Renamed during open? Retry
                        except Exception as e:
                            logging.error(f"Read error: {e}")
                            raise e

                # Check if download finished
                if download_task.done():
                    try:
                        download_task.result()
                        # If we are here, it means we consumed all available data
                        # Check if there is any final data in the final file
                        if os.path.exists(final_file_path):
                            final_size = os.path.getsize(final_file_path)
                            if final_size > current:
                                continue # Read remaining
                        break # Done
                    except Exception as e:
                        logging.error(f"Background download failed: {e}")
                        raise e
                
                # Wait for more data
                await asyncio.sleep(0.2)

        except Exception as e:
            logging.error(f"Streaming error: {e}")
            raise
        finally:
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
            if os.path.exists(temp_path + ".temp"):
                try:
                    os.remove(temp_path + ".temp")
                except OSError:
                    pass
