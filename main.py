import uvicorn
from fastapi import FastAPI
from bot_client import bot
from server.routes import router
from config import Config

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
        print("ERROR: API_ID, API_HASH, or BOT_TOKEN not found in .env file.")
        print("Please fill in your Telegram API details in the .env file.")
    else:
        from pyrogram.errors import FloodWait
        import asyncio
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await bot.start()
                print("Bot Started in FastAPI Loop")
                break
            except FloodWait as e:
                wait_time = e.value
                print(f"⚠️ FloodWait: Telegram requires a wait of {wait_time} seconds.")
                print(f"This happens when there are too many login attempts.")
                print(f"Waiting {wait_time} seconds before retry... (Attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
            except Exception as e:
                print(f"❌ Failed to start bot: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(5)
                else:
                    print("Max retries reached. Bot will not start.")
                    break
    
    yield
    
    try:
        await bot.stop()
        print("Bot Stopped")
    except Exception as e:
        print(f"Bot shutdown error (can be ignored): {e}")

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        workers=1
    )
