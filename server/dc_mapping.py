"""
DC Mapping - Tracks which DC each file/message belongs to
"""
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# Map (chat_id, message_id) -> dc_id
file_dc_mapping: Dict[Tuple[int, int], int] = {}


def set_file_dc(chat_id: int, message_id: int, dc_id: int) -> None:
    """
    Save the DC location for a specific file/message.
    
    Args:
        chat_id: Telegram chat ID
        message_id: Telegram message ID
        dc_id: Data center ID where the file is stored
    """
    key = (chat_id, message_id)
    file_dc_mapping[key] = dc_id
    logger.info(f"Saved mapping: Chat {chat_id}, Message {message_id} → DC {dc_id}")


def get_file_dc(chat_id: int, message_id: int) -> Optional[int]:
    """
    Get the DC location for a specific file/message.
    
    Args:
        chat_id: Telegram chat ID
        message_id: Telegram message ID
        
    Returns:
        DC ID if known, None otherwise
    """
    key = (chat_id, message_id)
    dc_id = file_dc_mapping.get(key)
    if dc_id:
        logger.debug(f"Found mapping: Chat {chat_id}, Message {message_id} → DC {dc_id}")
    return dc_id


def clear_mapping(chat_id: int, message_id: int) -> None:
    """
    Remove the DC mapping for a specific file/message.
    Useful if you need to re-detect the DC.
    
    Args:
        chat_id: Telegram chat ID
        message_id: Telegram message ID
    """
    key = (chat_id, message_id)
    if key in file_dc_mapping:
        del file_dc_mapping[key]
        logger.info(f"Cleared mapping for Chat {chat_id}, Message {message_id}")


def get_stats() -> Dict:
    """
    Get statistics about the DC mapping.
    
    Returns:
        Dictionary with mapping statistics
    """
    dc_counts = {}
    for (chat_id, msg_id), dc_id in file_dc_mapping.items():
        dc_counts[dc_id] = dc_counts.get(dc_id, 0) + 1
    
    return {
        "total_files": len(file_dc_mapping),
        "dc_distribution": dc_counts
    }
