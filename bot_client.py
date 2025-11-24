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
            workdir="."
        )
        self.boot_status = "Starting..."

    async def start(self):
        await super().start()
        print("Bot Started!")

    async def stop(self, *args):
        try:
            await super().stop()
            print("Bot Stopped!")
        except RuntimeError as e:
            # Suppress the "attached to a different loop" error
            if "attached to a different loop" not in str(e):
                raise

bot = Bot()
