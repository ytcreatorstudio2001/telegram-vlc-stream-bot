"""
Improved streaming routes with ByteStreamer integration
"""
import re
import math
import logging
import mimetypes
from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import StreamingResponse
from bot_client import bot
from server.byte_streamer import ByteStreamer

router = APIRouter()
logger = logging.getLogger(__name__)

# Global ByteStreamer instance (cached)
byte_streamer: ByteStreamer = None


async def get_byte_streamer() -> ByteStreamer:
    """Get or create ByteStreamer instance."""
    global byte_streamer
    if byte_streamer is None:
        byte_streamer = ByteStreamer(bot)
    return byte_streamer


@router.get("/stream/{chat_id}/{message_id}")
async def stream_media(chat_id: int, message_id: int, request: Request):
    """
    Stream media files from Telegram with Range request support.
    Uses ByteStreamer for efficient caching and session management.
    """
    logger.info(f"Stream request: Chat {chat_id}, Message {message_id}")
    
    if not bot.is_connected:
        logger.warning(f"Bot not connected. Status: {bot.boot_status}")
        raise HTTPException(status_code=503, detail=f"Bot Unavailable: {bot.boot_status}")

    # Get message and validate media
    try:
        msg = await bot.get_messages(chat_id, message_id)
    except Exception as e:
        logger.error(f"Failed to get message {message_id} from chat {chat_id}: {e}")
        raise HTTPException(status_code=404, detail="Message not found")

    if not msg or not msg.media:
        raise HTTPException(status_code=404, detail="No media found in message")

    # Extract media properties
    media = getattr(msg, msg.media.value)
    file_id = media.file_id
    file_size = media.file_size
    mime_type = getattr(media, "mime_type", "application/octet-stream")
    file_name = getattr(media, "file_name", "video.mp4")

    # Improve MIME type detection
    if mime_type == "application/octet-stream" and file_name:
        guessed_type, _ = mimetypes.guess_type(file_name)
        if guessed_type:
            mime_type = guessed_type

    # Parse Range header
    range_header = request.headers.get("range")
    start = 0
    end = file_size - 1

    if range_header:
        try:
            range_match = re.search(r"bytes=(\d+)-(\d*)", range_header)
            if range_match:
                start = int(range_match.group(1))
                if range_match.group(2):
                    end = int(range_match.group(2))
        except Exception as e:
            logger.warning(f"Failed to parse range header: {e}")

    # Validate range
    if start >= file_size or start < 0 or end >= file_size:
        return Response(
            status_code=416,
            headers={"Content-Range": f"bytes */{file_size}"}
        )

    # Calculate chunk parameters (aligned to 4096 bytes for Telegram)
    chunk_size = 1024 * 1024  # 1 MB chunks
    until_bytes = min(end, file_size - 1)
    
    # Align offset to chunk_size boundary
    offset = start - (start % chunk_size)
    first_part_cut = start - offset
    last_part_cut = (until_bytes % chunk_size) + 1
    
    # Calculate number of parts needed
    part_count = math.ceil((until_bytes + 1) / chunk_size) - math.floor(offset / chunk_size)
    req_length = until_bytes - start + 1

    logger.debug(
        f"Range: {start}-{until_bytes}/{file_size}, "
        f"Offset: {offset}, Parts: {part_count}, "
        f"First cut: {first_part_cut}, Last cut: {last_part_cut}"
    )

    # Get ByteStreamer instance
    streamer = await get_byte_streamer()
    
    # Get file properties (cached if available)
    try:
        file_props = await streamer.get_file_properties(chat_id, message_id)
    except Exception as e:
        logger.error(f"Failed to get file properties: {e}")
        raise HTTPException(status_code=500, detail="Failed to process file")

    # Stream generator using ByteStreamer
    async def stream_generator():
        try:
            async for chunk in streamer.yield_file(
                file_props,
                offset,
                first_part_cut,
                last_part_cut,
                part_count,
                chunk_size
            ):
                yield chunk
        except Exception as e:
            logger.exception(f"Streaming error: {e}")
            raise

    # Response headers
    headers = {
        "Content-Type": mime_type,
        "Content-Range": f"bytes {start}-{until_bytes}/{file_size}",
        "Content-Length": str(req_length),
        "Content-Disposition": f'inline; filename="{file_name}"',
        "Accept-Ranges": "bytes",
    }

    return StreamingResponse(
        stream_generator(),
        status_code=206 if range_header else 200,
        headers=headers,
        media_type=mime_type
    )


@router.get("/")
async def root():
    """Root endpoint with bot status."""
    return {
        "status": "running",
        "service": "Telegram Stream Bot",
        "version": "2.0.0",
        "bot_status": bot.boot_status if hasattr(bot, 'boot_status') else "Unknown",
        "features": [
            "Range request support",
            "File caching",
            "Media session management",
            "VLC compatible streaming"
        ],
        "message": "Send a file to the bot to get a stream link."
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if bot.is_connected else "unhealthy",
        "bot_connected": bot.is_connected,
        "bot_status": bot.boot_status if hasattr(bot, 'boot_status') else "Unknown"
    }
