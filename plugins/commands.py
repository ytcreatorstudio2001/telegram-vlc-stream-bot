import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Loading commands plugin...")

@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    logger.info(f"Received /start from {message.from_user.id}")
    await message.reply_text(
        "Hello! I am a Telegram File Streaming Bot.\n"
        "Send me any file, video, or audio, and I will generate a streamable link for VLC.\n\n"
        "Commands:\n"
        "/start - Check if I'm alive\n"
        "/stream - (Reply to a file) Get a stream link"
    )

@Client.on_message(filters.command("stream") & filters.reply)
async def stream_command(client: Client, message: Message):
    logger.info(f"Received /stream from {message.from_user.id}")
    msg = message.reply_to_message
    if not msg or not msg.media:
        await message.reply_text("Please reply to a message with media.")
        return

    await generate_and_send_link(message, msg)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_stream(client: Client, message: Message):
    logger.info(f"Received file from {message.from_user.id}")
    # Automatically generate link for private files
    await generate_and_send_link(message, message)

async def generate_and_send_link(reply_to: Message, media_msg: Message):
    # Get the file_id (works for document, video, audio)
    media = getattr(media_msg, media_msg.media.value)
    file_name = getattr(media, "file_name", "streamed_file")
    
    stream_link = f"{Config.URL}/stream/{media_msg.chat.id}/{media_msg.id}"
    
    await reply_to.reply_text(
        f"**Stream Link Generated!**\n\n"
        f"File Name: `{file_name}`\n"
        f"Stream URL:\n`{stream_link}`\n\n"
        f"**How to use in VLC:**\n"
        f"1. Open VLC\n"
        f"2. Go to Media > Open Network Stream\n"
        f"3. Paste the URL above\n"
        f"4. Click Play"
    )
