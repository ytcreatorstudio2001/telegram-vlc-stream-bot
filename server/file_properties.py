"""
File properties utilities - Extract metadata from Telegram messages
"""
import logging
from pyrogram import Client
from pyrogram.file_id import FileId
from pyrogram.types import Message

logger = logging.getLogger(__name__)


async def get_file_ids(client: Client, chat_id: int, message_id: int) -> FileId:
    """
    Get FileId object from a message.
    
    Args:
        client: Pyrogram client
        chat_id: Chat ID
        message_id: Message ID
        
    Returns:
        FileId: Decoded file ID with all properties
    """
    try:
        msg = await client.get_messages(chat_id, message_id)
        
        if not msg or not msg.media:
            return None
        
        media = getattr(msg, msg.media.value)
        file_id = FileId.decode(media.file_id)
        
        return file_id
    except Exception as e:
        logger.error(f"Failed to get file IDs: {e}")
        return None


def get_name(msg: Message) -> str:
    """
    Extract file name from message.
    
    Args:
        msg: Pyrogram message
        
    Returns:
        str: File name or default
    """
    if not msg or not msg.media:
        return "file"
    
    media = getattr(msg, msg.media.value)
    file_name = getattr(media, "file_name", None)
    
    if file_name:
        return file_name
    
    # Generate default name based on media type
    if msg.video:
        return "video.mp4"
    elif msg.audio:
        return "audio.mp3"
    elif msg.document:
        return "document.pdf"
    elif msg.photo:
        return "photo.jpg"
    else:
        return "file"


def get_hash(msg: Message) -> str:
    """
    Get unique hash for file verification.
    
    Args:
        msg: Pyrogram message
        
    Returns:
        str: First 6 characters of unique_id
    """
    if not msg or not msg.media:
        return ""
    
    media = getattr(msg, msg.media.value)
    file_id = FileId.decode(media.file_id)
    
    return file_id.unique_id[:6]


def get_media_file_size(msg: Message) -> int:
    """
    Get file size from message.
    
    Args:
        msg: Pyrogram message
        
    Returns:
        int: File size in bytes
    """
    if not msg or not msg.media:
        return 0
    
    media = getattr(msg, msg.media.value)
    return getattr(media, "file_size", 0)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size (e.g., "1.5 GB")
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"
