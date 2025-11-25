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
    
    # 1. Pre-create session file with correct DC ID to force connection to that DC
    session_name = f"persistent_dc_{dc_id}_v3" # Bump to v3 to be clean
    from pyrogram.storage import FileStorage
    
    # Manually create storage to set DC ID before Client init
    storage = FileStorage(name=session_name, workdir=SESSION_DIR)
    await storage.open()
    await storage.dc_id(dc_id)
    await storage.save()
    await storage.close()

    # 2. Initialize Client
    client = Client(
        name=session_name,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        workdir=SESSION_DIR,
        no_updates=True,
        plugins=None, # Disable plugins for these sub-clients
    )

    # 3. Connect (should now connect to target DC)
    try:
        await client.connect()
    except Exception as e:
        logger.error(f"Failed to connect to DC {dc_id}: {e}")
        raise RuntimeError(f"Failed to connect to DC {dc_id}: {e}")

    # 4. Authorize
    try:
        await client.get_me()
        logger.info(f"DC {dc_id} client already authorized")
    except Exception:
        logger.info(f"Authorizing DC {dc_id} client...")
        # Try ExportAuthorization first (works for some bot setups)
        try:
            main_client = await get_main_client()
            if not main_client.is_connected:
                await main_client.start()

            export_auth = await main_client.invoke(ExportAuthorization(dc_id=dc_id))
            
            await client.invoke(ImportAuthorization(
                id=export_auth.id, 
                bytes=export_auth.bytes
            ))
            logger.info(f"Successfully authorized on DC {dc_id} via ExportAuthorization")
            
        except (FloodWait, Exception) as e:
            logger.warning(f"ExportAuthorization failed ({e}), trying bot token login...")
            # Fallback: Login with bot token directly on this DC
            # This works if the bot is allowed to be on this DC (which it is, for downloading)
            try:
                await client.sign_in_bot(Config.BOT_TOKEN)
                logger.info(f"Successfully authorized on DC {dc_id} via Bot Token")
            except Exception as login_err:
                logger.error(f"All auth methods failed for DC {dc_id}: {login_err}")
                await client.disconnect()
                raise RuntimeError(f"All auth methods failed for DC {dc_id}: {login_err}")

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
