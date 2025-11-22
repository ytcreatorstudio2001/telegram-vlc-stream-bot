import re
from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import StreamingResponse
from bot_client import bot
from server.streamer import TelegramFileStreamer

router = APIRouter()

@router.get("/stream/{chat_id}/{message_id}")
async def stream_media(chat_id: int, message_id: int, request: Request):
    try:
        msg = await bot.get_messages(chat_id, message_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Message not found")

    if not msg or not msg.media:
        raise HTTPException(status_code=404, detail="No media found in message")

    media = getattr(msg, msg.media.value)
    file_id = media.file_id
    file_size = media.file_size
    mime_type = getattr(media, "mime_type", "application/octet-stream")
    file_name = getattr(media, "file_name", "video.mp4")

    # Fix MIME type for VLC if generic
    if mime_type == "application/octet-stream" and file_name:
        import mimetypes
        guessed_type, _ = mimetypes.guess_type(file_name)
        if guessed_type:
            mime_type = guessed_type

    # Handle Range Header
    range_header = request.headers.get("range")
    start = 0
    end = file_size - 1

    if range_header:
        try:
            # Parse "bytes=0-100"
            range_match = re.search(r"bytes=(\d+)-(\d*)", range_header)
            if range_match:
                start = int(range_match.group(1))
                if range_match.group(2):
                    end = int(range_match.group(2))
        except Exception:
            pass # Fallback to full file

    # Ensure valid range
    if start >= file_size or start < 0:
        return Response(status_code=416, headers={"Content-Range": f"bytes */{file_size}"})

    content_length = end - start + 1
    
    streamer = TelegramFileStreamer(bot, file_id, file_size)
    
    # Force linear streaming for now to prevent VLC seeking timeouts
    # We will re-enable seeking once linear playback is confirmed
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": mime_type,
        "Content-Disposition": f'inline; filename="{file_name}"'
    }

    return StreamingResponse(
        streamer.yield_chunks(start, end + 1),
        status_code=206 if range_header else 200,
        headers=headers,
        media_type=mime_type
    )

@router.get("/")
async def root():
    return {
        "status": "running",
        "service": "Telegram Stream Bot",
        "version": "1.0.0",
        "message": "Send a file to the bot to get a stream link."
    }
