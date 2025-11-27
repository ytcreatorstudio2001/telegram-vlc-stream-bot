import motor.motor_asyncio
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=id,
            join_date=None
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        """Get list of all user IDs"""
        users = []
        async for user in self.col.find({}):
            users.append(user['id'])
        return users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

db = None
if Config.DATABASE_URL:
    try:
        db = Database(Config.DATABASE_URL, "TelegramStreamBot")
        logger.info("Connected to MongoDB successfully!")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
else:
    logger.warning("DATABASE_URL not found! Using in-memory/file storage (not persistent on cloud).")
