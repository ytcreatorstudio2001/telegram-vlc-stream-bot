import logging
import uvicorn
from fastapi import FastAPI
from bot_client import bot
from server.routes import router
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
        print("ERROR: API_ID, API_HASH, or BOT_TOKEN not found in .env file.")
        print("Please fill in your Telegram API details in the .env file.")
    else:
        import asyncio
        
        async def start_bot_background():
            from pyrogram.errors import FloodWait
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    logger.info(f"Attempting to start bot (Attempt {attempt + 1}/{max_retries})...")
                    await bot.start()
                    logger.info("Bot Started in Background Loop")
                    print("Bot Started in Background Loop")
                    break
                except FloodWait as e:
                    wait_time = e.value
                    logger.warning(f"⚠️ FloodWait: Telegram requires a wait of {wait_time} seconds.")
                    print(f"Waiting {wait_time} seconds before retry...")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    logger.error(f"❌ Failed to start bot: {e}")
                    print(f"❌ Failed to start bot: {e}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                    else:
                        print("Max retries reached. Bot will not start.")
                        break

        # Start bot in background so Uvicorn can start immediately
        asyncio.create_task(start_bot_background())
    
    yield
    
    try:
        await bot.stop()
        print("Bot Stopped")
    except RuntimeError as e:
        # Ignore the "attached to a different loop" error during shutdown
        # This is a known issue with Pyrogram + FastAPI lifespan
        if "attached to a different loop" in str(e):
            print("Bot stopped (ignoring asyncio loop cleanup warning)")
        else:
            print(f"Bot shutdown error: {e}")
    except Exception as e:
        print(f"Bot shutdown error (can be ignored): {e}")

app = FastAPI(lifespan=lifespan)

# Add AI Error Handler Middleware
from server.error_handler import AIErrorMiddleware
app.add_middleware(AIErrorMiddleware)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        workers=1
    )
