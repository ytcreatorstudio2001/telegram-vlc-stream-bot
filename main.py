import uvicorn
from fastapi import FastAPI
from bot_client import bot
from server.routes import router
from config import Config

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
        print("ERROR: API_ID, API_HASH, or BOT_TOKEN not found in .env file.")
        print("Please fill in your Telegram API details in the .env file.")
        # We don't exit here to allow the server to start and show the error in logs,
        # but the bot won't start properly.
        return

    await bot.start()
    print("Bot Started in FastAPI Loop")

@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()
    print("Bot Stopped")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT
    )
