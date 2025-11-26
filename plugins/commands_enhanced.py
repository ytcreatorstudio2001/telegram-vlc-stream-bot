"""
Enhanced commands plugin with batch support, better link generation, and file info
"""
import os
import re
import json
import base64
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from config import Config
from urllib.parse import quote_plus
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Loading enhanced commands plugin...")


def get_file_info(media_msg: Message) -> dict:
    """Extract file information from message."""
    if not media_msg or not media_msg.media:
        return {}
    
    media = getattr(media_msg, media_msg.media.value)
    
    return {
        "file_name": getattr(media, "file_name", "Unknown"),
        "file_size": getattr(media, "file_size", 0),
        "mime_type": getattr(media, "mime_type", "Unknown"),
        "duration": getattr(media, "duration", 0) if hasattr(media, "duration") else 0,
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"


def format_duration(seconds: int) -> str:
    """Format duration in HH:MM:SS."""
    if seconds == 0:
        return "N/A"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    """Start command with welcome message."""
    logger.info(f"Received /start from {message.from_user.id}")
    
    await message.reply_text(
        "🎬 **Welcome to Telegram Stream Bot!**\n\n"
        "I can generate streamable links for your media files.\n\n"
        "**📋 Commands:**\n"
        "• `/start` - Show this message\n"
        "• `/stream` - Reply to a file to get stream link\n"
        "• `/batch` - Generate links for multiple files\n"
        "• `/help` - Detailed help\n\n"
        "**💡 Quick Start:**\n"
        "Just send me any video, audio, or document file!\n\n"
        "**🎯 Features:**\n"
        "✅ VLC compatible streaming\n"
        "✅ Range request support (seeking)\n"
        "✅ Batch link generation\n"
        "✅ Fast and reliable\n\n"
        f"**🔗 Base URL:** `{Config.URL}`",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Detailed help command."""
    await message.reply_text(
        "📚 **Detailed Help**\n\n"
        "**How to use:**\n\n"
        "1️⃣ **Single File:**\n"
        "   • Send any file to the bot\n"
        "   • You'll receive a stream link\n"
        "   • Copy and paste in VLC\n\n"
        "2️⃣ **Using /stream:**\n"
        "   • Reply to any file with `/stream`\n"
        "   • Get stream link instantly\n\n"
        "3️⃣ **Batch Links:**\n"
        "   • Use `/batch <first_link> <last_link>`\n"
        "   • Example: `/batch https://t.me/c/123/10 https://t.me/c/123/20`\n"
        "   • Generate links for multiple files at once\n\n"
        "**VLC Setup:**\n"
        "1. Open VLC Media Player\n"
        "2. Go to Media → Open Network Stream\n"
        "3. Paste the stream URL\n"
        "4. Click Play\n\n"
        "**Supported Formats:**\n"
        "✅ Videos (MP4, MKV, AVI, etc.)\n"
        "✅ Audio (MP3, FLAC, WAV, etc.)\n"
        "✅ Documents\n\n"
        "Need more help? Contact support!",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("stream") & filters.reply)
async def stream_command(client: Client, message: Message):
    """Generate stream link for replied message."""
    logger.info(f"Received /stream from {message.from_user.id}")
    
    msg = message.reply_to_message
    if not msg or not msg.media:
        await message.reply_text("❌ Please reply to a message with media.")
        return

    await generate_and_send_link(message, msg)


@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_stream(client: Client, message: Message):
    """Automatically generate link for private files."""
    logger.info(f"Received file from {message.from_user.id}")
    await generate_and_send_link(message, message)


async def generate_and_send_link(reply_to: Message, media_msg: Message):
    """Generate and send stream link with file info."""
    file_info = get_file_info(media_msg)
    
    if not file_info:
        await reply_to.reply_text("❌ No media found in this message.")
        return
    
    # Generate stream link
    stream_link = f"{Config.URL}/stream/{media_msg.chat.id}/{media_msg.id}"
    file_name = file_info.get("file_name", "Unknown")
    file_name_encoded = quote_plus(file_name)
    
    # Create inline buttons
    buttons = [
        [
            InlineKeyboardButton("📥 Download", url=stream_link),
            InlineKeyboardButton("▶️ Stream", url=stream_link)
        ]
    ]
    
    # Format message
    message_text = (
        "✅ **Stream Link Generated!**\n\n"
        f"📄 **File:** `{file_name}`\n"
        f"📦 **Size:** `{format_file_size(file_info.get('file_size', 0))}`\n"
    )
    
    if file_info.get("duration", 0) > 0:
        message_text += f"⏱️ **Duration:** `{format_duration(file_info['duration'])}`\n"
    
    if file_info.get("mime_type") != "Unknown":
        message_text += f"🎬 **Type:** `{file_info['mime_type']}`\n"
    
    message_text += (
        f"\n🔗 **Stream URL:**\n`{stream_link}`\n\n"
        "**📺 How to use in VLC:**\n"
        "1. Open VLC Media Player\n"
        "2. Media → Open Network Stream\n"
        "3. Paste the URL above\n"
        "4. Click Play\n\n"
        "💡 **Tip:** You can seek/forward in the video!"
    )
    
    await reply_to.reply_text(
        message_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("batch"))
async def batch_command(client: Client, message: Message):
    """
    Generate batch links for multiple messages.
    Usage: /batch <first_link> <last_link>
    Example: /batch https://t.me/c/123456/10 https://t.me/c/123456/20
    """
    logger.info(f"Received /batch from {message.from_user.id}")
    
    if " " not in message.text:
        await message.reply_text(
            "❌ **Invalid format!**\n\n"
            "**Usage:** `/batch <first_link> <last_link>`\n\n"
            "**Example:**\n"
            "`/batch https://t.me/c/123456/10 https://t.me/c/123456/20`\n\n"
            "This will generate stream links for messages 10 to 20."
        )
        return
    
    links = message.text.strip().split(" ")
    if len(links) != 3:
        await message.reply_text(
            "❌ **Invalid format!**\n\n"
            "Please provide exactly 2 links (first and last message)."
        )
        return
    
    cmd, first_link, last_link = links
    
    # Parse Telegram links
    regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
    
    first_match = regex.match(first_link)
    last_match = regex.match(last_link)
    
    if not first_match or not last_match:
        await message.reply_text("❌ Invalid Telegram link format!")
        return
    
    # Extract chat and message IDs
    first_chat_id = first_match.group(4)
    first_msg_id = int(first_match.group(5))
    
    last_chat_id = last_match.group(4)
    last_msg_id = int(last_match.group(5))
    
    # Convert chat ID if numeric (private channel)
    if first_chat_id.isnumeric():
        first_chat_id = int("-100" + first_chat_id)
    if last_chat_id.isnumeric():
        last_chat_id = int("-100" + last_chat_id)
    
    if first_chat_id != last_chat_id:
        await message.reply_text("❌ Both links must be from the same chat!")
        return
    
    if first_msg_id > last_msg_id:
        await message.reply_text("❌ First message ID must be less than last message ID!")
        return
    
    # Generate links
    sts = await message.reply_text("🔄 **Generating batch links...**\n\nPlease wait...")
    
    total_messages = last_msg_id - first_msg_id + 1
    links_generated = []
    
    try:
        for msg_id in range(first_msg_id, last_msg_id + 1):
            try:
                msg = await client.get_messages(first_chat_id, msg_id)
                
                if msg and msg.media:
                    file_info = get_file_info(msg)
                    stream_link = f"{Config.URL}/stream/{first_chat_id}/{msg_id}"
                    
                    links_generated.append({
                        "message_id": msg_id,
                        "file_name": file_info.get("file_name", "Unknown"),
                        "file_size": file_info.get("file_size", 0),
                        "stream_link": stream_link
                    })
                
                # Update progress every 10 messages
                if len(links_generated) % 10 == 0:
                    await sts.edit_text(
                        f"🔄 **Generating batch links...**\n\n"
                        f"Progress: {len(links_generated)}/{total_messages}"
                    )
                
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                logger.error(f"Error processing message {msg_id}: {e}")
                continue
        
        # Create result file
        if links_generated:
            result_text = "✅ **Batch Links Generated!**\n\n"
            result_text += f"**Total Files:** {len(links_generated)}\n\n"
            
            for idx, link_data in enumerate(links_generated, 1):
                result_text += (
                    f"{idx}. **{link_data['file_name']}**\n"
                    f"   Size: {format_file_size(link_data['file_size'])}\n"
                    f"   Link: `{link_data['stream_link']}`\n\n"
                )
            
            # If too long, save to file
            if len(result_text) > 4000:
                file_name = f"batch_links_{message.from_user.id}.txt"
                with open(file_name, "w", encoding="utf-8") as f:
                    for link_data in links_generated:
                        f.write(f"{link_data['file_name']}\n")
                        f.write(f"{link_data['stream_link']}\n\n")
                
                await message.reply_document(
                    file_name,
                    caption=f"✅ **Batch Links Generated!**\n\n**Total Files:** {len(links_generated)}"
                )
                os.remove(file_name)
            else:
                await sts.edit_text(result_text, disable_web_page_preview=True)
        else:
            await sts.edit_text("❌ No media files found in the specified range!")
    
    except Exception as e:
        logger.error(f"Batch generation error: {e}")
        await sts.edit_text(f"❌ **Error:** {str(e)}")


print("Enhanced commands plugin loaded successfully!")
