"""
DC Manager - Handles multi-DC client creation and FloodWait tracking
"""
import time
import logging
import os
import asyncio
from typing import Dict
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.raw.functions.auth import ExportAuthorization, ImportAuthorization
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)

# Session directory for persistent storage
SESSION_DIR = os.getenv("SESSION_DIR", "/app/sessions" if os.path.exists("/app/sessions") else ".")
os.makedirs(SESSION_DIR, exist_ok=True)

# Global registries
dc_clients: Dict[int, Client] = {}  # dc_id -> Client
dc_flood_until: Dict[int, float] = {}  # dc_id -> unix timestamp when FloodWait ends

MAIN_DC_ID = 5  # Main bot DC (Observed from logs)

async def get_main_client() -> Client:
    """Return the main client (single session, main DC).
    Reuses existing client if already created.
    """
    if MAIN_DC_ID in dc_clients:
        return dc_clients[MAIN_DC_ID]
    # Import here to avoid circular dependency
    from bot_client import bot
    dc_clients[MAIN_DC_ID] = bot
    return bot

async def get_dc_client(dc_id: int) -> Client:
    """Get or create a client for a specific DC.
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
    logger.info(f"Creating client for DC {dc_id}")
    
    # Use in-memory session for DC clients to avoid filesystem issues on Koyeb
    # This is more reliable for temporary DC clients used only for file streaming
    session_name = f":memory:"  # In-memory session
    
    # Initialize Client with in_memory flag
    client = Client(
        name=f"dc_{dc_id}_client",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,  # Use bot token directly
        in_memory=True,  # Don't persist session to disk
        no_updates=True,
        plugins=None,  # Disable plugins for these sub-clients
    )

    # 3. Start the client (handles connection and authorization automatically)
    try:
        await client.start()
        logger.info(f"Successfully started and authorized DC {dc_id} client")
    except FloodWait as fw:
        logger.error(f"FloodWait when starting DC {dc_id} client: {fw.value}s")
        dc_flood_until[dc_id] = time.time() + fw.value
        await client.stop()
        raise RuntimeError(f"FloodWait for DC {dc_id}: {fw.value}s")
    except Exception as e:
        logger.error(f"Failed to start DC {dc_id} client: {e}")
        try:
            await client.stop()
        except:
            pass
        raise RuntimeError(f"Failed to start DC {dc_id} client: {e}")

    dc_clients[dc_id] = client
    return client

async def cleanup_dc_clients():
    """Stop all DC clients gracefully.
    Call this on application shutdown.
    """
    for dc_id, client in dc_clients.items():
        try:
            await client.stop()
            logger.info(f"Stopped DC {dc_id} client")
        except Exception as e:
            logger.error(f"Error stopping DC {dc_id} client: {e}")

async def invalidate_dc_client(dc_id: int):
    """Remove a DC client from cache, forcing reconnection next time."""
    if dc_id in dc_clients:
        client = dc_clients.pop(dc_id)
        try:
            await client.stop()
        except Exception:
            pass
        logger.warning(f"Invalidated and stopped cached client for DC {dc_id}")
