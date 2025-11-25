"""
DC Manager - Handles multi-DC client creation and FloodWait tracking
"""
import time
import logging
import os
from typing import Dict
from pyrogram import Client
from pyrogram.errors import FloodWait
from config import Config

logger = logging.getLogger(__name__)

# Session directory for persistent storage
SESSION_DIR = os.getenv("SESSION_DIR", "/app/sessions" if os.path.exists("/app/sessions") else ".")
os.makedirs(SESSION_DIR, exist_ok=True)

# Global registries
dc_clients: Dict[int, Client] = {}  # dc_id -> Client
dc_flood_until: Dict[int, float] = {}  # dc_id -> unix timestamp when FloodWait ends

MAIN_DC_ID = 2  # Main bot DC (adjust if different)


async def get_main_client() -> Client:
    """
    Return the main client (single session, main DC).
    Reuses existing client if already created.
    """
    if MAIN_DC_ID in dc_clients:
        return dc_clients[MAIN_DC_ID]

    # Import here to avoid circular dependency
    from bot_client import bot
    dc_clients[MAIN_DC_ID] = bot
    return bot


async def get_dc_client(dc_id: int) -> Client:
    """
    Get or create a client for a specific DC.
    Respects FloodWait: if we are in a wait window, raises RuntimeError.
    
    Args:
        dc_id: Target data center ID
        
    Returns:
        Client instance for the specified DC
        
    Raises:
        RuntimeError: If DC is in FloodWait period or client creation fails
    """
    # Check if we're in FloodWait period for this DC
    now = time.time()
    flood_end = dc_flood_until.get(dc_id, 0)
    if now < flood_end:
        wait_sec = int(flood_end - now)
        msg = f"DC {dc_id} is in FloodWait; try again after {wait_sec} seconds"
        logger.warning(msg)
        raise RuntimeError(msg)

    # Return existing client if available
    if dc_id in dc_clients:
        logger.info(f"Reusing existing client for DC {dc_id}")
        return dc_clients[dc_id]

    # Create new client for this DC
    logger.info(f"Creating and starting client for DC {dc_id}")
    client = Client(
        name=f"persistent_dc_{dc_id}",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        workdir=SESSION_DIR,
        no_updates=True
    )

    # Set DC ID if session doesn't exist
    session_path = os.path.join(SESSION_DIR, f"persistent_dc_{dc_id}.session")
    if not os.path.exists(session_path):
        logger.info(f"Setting DC ID {dc_id} for new session")
        await client.storage.open()
    return client


async def cleanup_dc_clients():
    """
    Stop all DC clients gracefully.
    Call this on application shutdown.
    """
    for dc_id, client in dc_clients.items():
        try:
            await client.stop()
            logger.info(f"Stopped DC {dc_id} client")
        except Exception as e:
            logger.error(f"Error stopping DC {dc_id} client: {e}")
