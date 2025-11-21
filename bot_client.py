from pyrogram import Client
from pyrogram.storage import MemoryStorage
from config import Config

class Bot(Client):
    def __init__(self):
        super().__init__(
            "TelegramStreamBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
            in_memory=True
        )

    async def start(self):
        await super().start()
        print("Bot Started!")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped!")

bot = Bot()
