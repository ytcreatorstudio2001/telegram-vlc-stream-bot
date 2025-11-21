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
        await bot.start()
        print("Bot Started in FastAPI Loop")
    
    yield
    
    await bot.stop()
    print("Bot Stopped")

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        workers=1
    )
