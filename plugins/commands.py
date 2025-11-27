"""
Telegram VLC Stream Bot - Commands Plugin
Copyright (c) 2025 Akhil TG. All Rights Reserved.

Enhanced commands plugin with batch support, better link generation, and file info
"""
import os
import re
import json
import base64
import logging
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
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
    """Start command with minimal colorful welcome message."""
    logger.info(f"Received /start from {message.from_user.id}")
    
    # Random banner selection
    banners = ["assets/banner.png", "assets/banner1.png", "assets/banner2.png", "assets/banner3.png"]
    selected_banner = random.choice(banners)
    
    # Create inline keyboard buttons
    buttons = [
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("🤖 Bot Info", callback_data="bot_info"),
            InlineKeyboardButton("👨‍💻 Owner Info", callback_data="owner_info")
        ],
        [
            InlineKeyboardButton("🔗 GitHub", url="https://github.com/ytcreatorstudio2001/telegram-vlc-stream-bot"),
            InlineKeyboardButton("📢 Updates", url="https://t.me/akhil_tg")
        ]
    ]
    
    # Minimal colorful welcome text
    welcome_text = (
        "**🎬 VLC Stream Bot**\n\n"
        f"👋 Hey **{message.from_user.first_name}**!\n\n"
        "**Stream Telegram files instantly** 🚀\n"
        "No downloads • Fast • Secure\n\n"
        "**Quick Start:**\n"
        "📤 Send any file → Get stream link\n"
        "🎥 Open in VLC → Enjoy!\n\n"
        "**Commands:**\n"
        "`/stream` • `/batch` • `/help` • `/about`\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "_© 2025 Akhil TG_"
    )
    
    # Send random banner with welcome message
    try:
        await message.reply_photo(
            photo=selected_banner,
            caption=welcome_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.error(f"Error sending banner: {e}")
        # Fallback to text-only message
        await message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(buttons),
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
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "**👨‍💻 Developer:** Akhil TG\n"
        "**© 2025** All Rights Reserved",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("about"))
async def about_command(client: Client, message: Message):
    """About command with bot and developer information."""
    await message.reply_text(
        "ℹ️ **About Telegram VLC Stream Bot**\n\n"
        "**🎬 What is this bot?**\n"
        "This bot allows you to stream large media files from Telegram "
        "directly to VLC or any media player without downloading the entire file. "
        "Perfect for watching movies, listening to music, or accessing large files on the go!\n\n"
        "**✨ Key Features:**\n"
        "• 🚀 Direct streaming without full download\n"
        "• ⏯️ Seek/Resume support (HTTP Range Headers)\n"
        "• 📱 Universal compatibility (VLC, MX Player, Browsers)\n"
        "• 💾 Handles large files (2GB+)\n"
        "• ⚡ Fast and efficient streaming\n"
        "• 🔒 Secure - no data storage\n"
        "• 📦 Batch link generation\n\n"
        "**🛠️ Technology Stack:**\n"
        "• Python 3.8+\n"
        "• FastAPI Framework\n"
        "• Pyrogram Library\n"
        "• Uvicorn Server\n\n"
        "**📊 Version:** 2.0.0\n"
        f"**🌐 Server:** `{Config.URL}`\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "**👨‍💻 Developer & Owner**\n"
        "**Name:** Akhil TG\n"
        "**Copyright:** © 2025 Akhil TG\n"
        "**License:** All Rights Reserved\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "**💡 Support the Project:**\n"
        "If you find this bot useful, please star the repository on GitHub!\n\n"
        "**⚠️ Disclaimer:**\n"
        "This bot is for personal use only. Please respect copyright laws "
        "and only stream content you have the right to access.",
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
    """Automatically generate link for private files (sent or forwarded)."""
    is_forwarded = message.forward_date is not None
    logger.info(f"Received file from {message.from_user.id} (forwarded: {is_forwarded})")
    await generate_and_send_link(message, message)


async def generate_and_send_link(reply_to: Message, media_msg: Message):
    """Generate and send stream link with beautiful formatting."""
    file_info = get_file_info(media_msg)
    
    if not file_info:
        await reply_to.reply_text("❌ No media found in this message.")
        return
    
    # Generate stream link
    stream_link = f"{Config.URL}/stream/{media_msg.chat.id}/{media_msg.id}"
    file_name = file_info.get("file_name", "Unknown")
    file_size = file_info.get('file_size', 0)
    duration = file_info.get("duration", 0)
    mime_type = file_info.get("mime_type", "Unknown")
    
    # Determine file type emoji
    file_type_emoji = "📄"
    if "video" in mime_type.lower():
        file_type_emoji = "🎬"
    elif "audio" in mime_type.lower():
        file_type_emoji = "🎵"
    elif "image" in mime_type.lower():
        file_type_emoji = "🖼️"
    
    # Create beautiful inline buttons
    buttons = [
        [
            InlineKeyboardButton("📥 Download", url=stream_link),
            InlineKeyboardButton("▶️ Stream in VLC", url=stream_link)
        ]
    ]
    
    # Beautiful formatted message with better visual hierarchy
    message_text = (
        "╔═══════════════════════╗\n"
        "║   ✨ **STREAM READY** ✨   ║\n"
        "╚═══════════════════════╝\n\n"
        f"{file_type_emoji} **File Information**\n"
        f"┣━ � Name: `{file_name}`\n"
        f"┣━ 📦 Size: `{format_file_size(file_size)}`\n"
    )
    
    if duration > 0:
        message_text += f"┣━ ⏱️ Duration: `{format_duration(duration)}`\n"
    
    if mime_type != "Unknown":
        message_text += f"┗━ 🎬 Type: `{mime_type}`\n"
    else:
        message_text += "┗━━━━━━━━━━━━━━━━━━━━\n"
    
    message_text += (
        f"\n🔗 **Stream URL**\n"
        f"```\n{stream_link}\n```\n\n"
        "📺 **Quick Start Guide**\n"
        "┣━ **VLC**: Media → Network Stream → Paste URL\n"
        "┣━ **Browser**: Click Download/Stream button\n"
        "┗━ **Mobile**: Use MX Player or VLC\n\n"
        "💡 **Features**\n"
        "✅ Instant streaming • No download needed\n"
        "✅ Seek/Forward support • Resume anytime\n"
        "✅ Works on all devices • Fast & secure\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "_Powered by VLC Stream Bot • © 2025 Akhil TG_"
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



# Callback Query Handlers for Inline Buttons

@Client.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    """Handle inline button callbacks."""
    data = callback_query.data
    
    # Back button
    back_button = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="start")]]
    
    if data == "start":
        # Show welcome message again with random banner
        banners = ["assets/banner.png", "assets/banner1.png", "assets/banner2.png", "assets/banner3.png"]
        selected_banner = random.choice(banners)
        
        buttons = [
            [
                InlineKeyboardButton("📚 Help", callback_data="help"),
                InlineKeyboardButton("ℹ️ About", callback_data="about")
            ],
            [
                InlineKeyboardButton("🤖 Bot Info", callback_data="bot_info"),
                InlineKeyboardButton("👨‍💻 Owner Info", callback_data="owner_info")
            ],
            [
                InlineKeyboardButton("🔗 GitHub", url="https://github.com/ytcreatorstudio2001/telegram-vlc-stream-bot"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/akhil_tg")
            ]
        ]
        
        welcome_text = (
            "**🎬 VLC Stream Bot**\n\n"
            f"👋 Hey **{callback_query.from_user.first_name}**!\n\n"
            "**Stream Telegram files instantly** 🚀\n"
            "No downloads • Fast • Secure\n\n"
            "**Quick Start:**\n"
            "📤 Send any file → Get stream link\n"
            "🎥 Open in VLC → Enjoy!\n\n"
            "**Commands:**\n"
            "`/stream` • `/batch` • `/help` • `/about`\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "_© 2025 Akhil TG_"
        )
        
        await callback_query.edit_message_media(
            media=InputMediaPhoto(
                media=selected_banner,
                caption=welcome_text
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif data == "help":
        help_text = (
            "📚 **Help Guide** 📚\n\n"
            "**🎯 How to Use:**\n"
            "1️⃣ Send any file → Get link instantly\n"
            "2️⃣ Reply to file with `/stream`\n"
            "3️⃣ Use `/batch <link1> <link2>` for multiple files\n\n"
            "**📺 VLC Setup:**\n"
            "Media → Open Network Stream → Paste URL → Play\n\n"
            "**🎬 Supported:**\n"
            "✅ Videos (MP4, MKV, AVI, etc.)\n"
            "✅ Audio (MP3, FLAC, WAV, etc.)\n"
            "✅ All file types\n\n"
            "💡 **Tips:** Seek/forward works • No size limits\n\n"
            "© 2025 Akhil TG"
        )
        
        await callback_query.edit_message_caption(
            caption=help_text,
            reply_markup=InlineKeyboardMarkup(back_button)
        )
    
    elif data == "about":
        about_text = (
            "ℹ️ **About** ℹ️\n\n"
            "Stream Telegram files directly to VLC without downloading!\n\n"
            "**✨ Features:**\n"
            "🚀 Direct streaming\n"
            "⏯️ Seek/Resume support\n"
            "📱 Universal compatibility\n"
            "💾 Large files (2GB+)\n"
            "⚡ Fast & efficient\n"
            "🔒 Secure - no storage\n"
            "📦 Batch generation\n\n"
            "**🛠️ Tech Stack:**\n"
            "Python • FastAPI • Pyrogram • Uvicorn\n\n"
            "**📊 Info:**\n"
            f"Version: 2.0.0 • Server: {Config.URL}\n"
            "Status: 🟢 Online • Uptime: 24/7\n\n"
            "© 2025 Akhil TG"
        )
        
        await callback_query.edit_message_caption(
            caption=about_text,
            reply_markup=InlineKeyboardMarkup(back_button)
        )
    
    elif data == "bot_info":
        bot_me = await client.get_me()
        bot_info_text = (
            "🤖 **Bot Info** 🤖\n\n"
            f"**Name:** {bot_me.first_name}\n"
            f"**Username:** @{bot_me.username}\n"
            f"**ID:** `{bot_me.id}`\n"
            f"**Version:** 2.0.0\n"
            f"**Status:** 🟢 Active\n\n"
            "**🌐 Server:**\n"
            f"URL: `{Config.URL}`\n"
            "Framework: FastAPI\n"
            "Library: Pyrogram\n\n"
            "**⚙️ Capabilities:**\n"
            "✅ Video/Audio streaming\n"
            "✅ Batch processing\n"
            "✅ HTTP Range support\n"
            "✅ Multi-DC support\n\n"
            "**📊 Performance:**\n"
            "Max Size: Unlimited\n"
            "Response: <100ms\n"
            "Uptime: 99.9%\n\n"
            "**🔐 Security:**\n"
            "No storage • Secure • Private\n\n"
            "© 2025 Akhil TG"
        )
        
        await callback_query.edit_message_caption(
            caption=bot_info_text,
            reply_markup=InlineKeyboardMarkup(back_button)
        )
    
    elif data == "owner_info":
        owner_buttons = [
            [
                InlineKeyboardButton("🔗 GitHub", url="https://github.com/ytcreatorstudio2001"),
                InlineKeyboardButton("📢 Telegram", url="https://t.me/akhil_tg")
            ],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")]
        ]
        
        owner_info_text = (
            "👨‍💻 **Owner Info** 👨‍💻\n\n"
            "**Name:** Akhil TG\n"
            "**Role:** Full Stack Developer\n"
            "**Location:** India 🇮🇳\n\n"
            "**💼 Skills:**\n"
            "🔹 Backend: Python, FastAPI, Node.js\n"
            "🔹 Frontend: React, Next.js\n"
            "🔹 DevOps: Docker, AWS, Koyeb\n"
            "🔹 Bots: Pyrogram, Telethon\n\n"
            "**🚀 Projects:**\n"
            "• VLC Stream Bot\n"
            "• Telegram Bots\n"
            "• Web Apps\n"
            "• Open Source\n\n"
            "**📫 Contact:**\n"
            "Telegram: @akhil_tg\n"
            "GitHub: @ytcreatorstudio2001\n\n"
            "**⭐ Support:**\n"
            "Star on GitHub • Share • Feedback\n\n"
            "© 2025 Akhil TG\n"
            "_Made with ❤️ in India_"
        )
        
        await callback_query.edit_message_caption(
            caption=owner_info_text,
            reply_markup=InlineKeyboardMarkup(owner_buttons)
        )
    
    # Answer the callback query
    await callback_query.answer()


print("Enhanced commands plugin loaded successfully!")

