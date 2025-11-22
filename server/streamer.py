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
        """
        # Create a temp file path (but don't create the file yet)
        # We want Pyrogram to create it
        fd, temp_path = tempfile.mkstemp()
        os.close(fd)
        os.remove(temp_path) # Remove it so Pyrogram can create it
        
        download_task = None
        
        try:
            # Start download in background
            download_task = asyncio.create_task(
                self.client.download_media(self.file_id, file_name=temp_path)
            )
            
            current = start
            
            # Pyrogram appends .temp to the filename while downloading
            temp_file_path = temp_path + ".temp"
            final_file_path = temp_path
            
            # Loop until we have served the requested range
            while current < end:
                # Determine which file to read from
                active_path = None
                if os.path.exists(temp_file_path):
                    active_path = temp_file_path
                elif os.path.exists(final_file_path):
                    active_path = final_file_path
                
                file_size_on_disk = 0
                if active_path:
                    file_size_on_disk = os.path.getsize(active_path)

                # If we have data to read
                if file_size_on_disk > current:
                    available = file_size_on_disk - current
                    to_read = min(self.chunk_size, available, end - current)
                    
                    if to_read > 0:
                        with open(active_path, "rb") as f:
                            f.seek(current)
                            chunk = f.read(to_read)
                            if chunk:
                                yield chunk
                                current += len(chunk)
                                continue

                # Check if download finished or failed
                if download_task.done():
                    try:
                        download_task.result() # Raise exception if failed
                        
                        # If download finished, the file should be at final_file_path
                        if os.path.exists(final_file_path):
                            final_size = os.path.getsize(final_file_path)
                            if final_size > current:
                                # Read remaining data from final file
                                continue
                            else:
                                break # Done
                        elif os.path.exists(temp_file_path):
                             # Should not happen if done, but just in case
                             pass
                        else:
                             # File missing?
                             break
                    except Exception as e:
                        logging.error(f"Background download failed: {e}")
                        raise e
                
                # Wait for more data
                await asyncio.sleep(0.5)

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
            if os.path.exists(temp_path + ".temp"):
                try:
                    os.remove(temp_path + ".temp")
                except OSError:
                    pass
