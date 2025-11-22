import math
import logging
import asyncio
from pyrogram import Client
from pyrogram.file_id import FileId

class StreamBuffer:
    """
    A file-like object that writes to an asyncio.Queue.
    Used to pipe Pyrogram's download_media directly to the streaming response.
    """
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def write(self, data: bytes):
        # This method is called by Pyrogram's downloader
        # We put the chunk into the queue
        # Note: This is called from a sync context in Pyrogram's worker, 
        # but we need to put it in an async queue.
        # Since Pyrogram runs in an asyncio loop, we can use call_soon_threadsafe 
        # or just put_nowait if the queue is unbounded.
        try:
            self.queue.put_nowait(data)
        except asyncio.QueueFull:
            # Should not happen with unbounded queue
            pass
        return len(data)

    def flush(self):
        pass

    def close(self):
        pass

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
        Stream file using a Queue buffer.
        Pyrogram downloads to the queue, we yield from the queue.
        """
        queue = asyncio.Queue()
        stream_buffer = StreamBuffer(queue)
        
        # Start download in background
        download_task = asyncio.create_task(
            self.client.download_media(
                self.file_id,
                file_name=stream_buffer, # Pass our custom buffer
                in_memory=True # Tell Pyrogram to treat file_name as a file-like object
            )
        )
        
        current = 0
        # We need to skip 'start' bytes
        bytes_to_skip = start
        
        try:
            while current < end:
                # Wait for data from the queue
                # We use a timeout to detect if download stalled
                try:
                    # If download is done and queue is empty, we are done
                    if download_task.done() and queue.empty():
                        # Check for exceptions
                        if download_task.exception():
                            raise download_task.exception()
                        break

                    # Wait for next chunk
                    chunk = await asyncio.wait_for(queue.get(), timeout=5.0)
                    
                    # Handle skipping for range requests
                    if bytes_to_skip > 0:
                        if len(chunk) <= bytes_to_skip:
                            bytes_to_skip -= len(chunk)
                            current += len(chunk)
                            continue
                        else:
                            chunk = chunk[bytes_to_skip:]
                            current += bytes_to_skip
                            bytes_to_skip = 0
                    
                    # Truncate if we go past 'end'
                    if current + len(chunk) > end:
                        chunk = chunk[:end - current]
                    
                    yield chunk
                    current += len(chunk)
                    
                except asyncio.TimeoutError:
                    if download_task.done():
                        if download_task.exception():
                            raise download_task.exception()
                        break
                    # Just a timeout waiting for network, continue waiting
                    continue
                    
        except Exception as e:
            logging.error(f"Streaming error: {e}")
            raise
        finally:
            if not download_task.done():
                download_task.cancel()
                try:
                    await download_task
                except asyncio.CancelledError:
                    pass
