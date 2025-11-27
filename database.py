import motor.motor_asyncio
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, uri, database_name):
        try:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                uri,
                serverSelectionTimeoutMS=2000,  # Reduced to 2 seconds
                connectTimeoutMS=2000,
                socketTimeoutMS=2000,
                retryWrites=True,
                w='majority',
                maxPoolSize=10,  # Connection pooling
                minPoolSize=1
            )
            self.db = self._client[database_name]
            self.col = self.db.users
            self.connected = True
            self._connection_checked = False
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB client: {e}")
            self.connected = False
            self._connection_checked = True

    async def _check_connection(self):
        """Check connection status once and cache result"""
        if self._connection_checked:
            return self.connected
        
        try:
            # Quick ping to verify connection
            await self._client.admin.command('ping')
            self.connected = True
            self._connection_checked = True
            logger.info("MongoDB connection verified")
        except Exception as e:
            logger.warning(f"MongoDB not available: {e}")
            self.connected = False
            self._connection_checked = True
        
        return self.connected

    def new_user(self, id):
        return dict(
            id=id,
            join_date=None
        )

    async def add_user(self, id):
        try:
            if not await self._check_connection():
                return False
            user = self.new_user(id)
            # Use insert_one without waiting for acknowledgment for speed
            await self.col.insert_one(user)
            return True
        except Exception as e:
            # Don't log every duplicate key error
            if "duplicate" not in str(e).lower():
                logger.error(f"Error adding user to MongoDB: {e}")
            return False

    async def is_user_exist(self, id):
        try:
            if not await self._check_connection():
                return False
            user = await self.col.find_one({'id': int(id)})
            return True if user else False
        except Exception as e:
            logger.error(f"Error checking user existence in MongoDB: {e}")
            return False

    async def total_users_count(self):
        try:
            if not await self._check_connection():
                return 0
            count = await self.col.count_documents({})
            return count
        except Exception as e:
            logger.error(f"Error counting users in MongoDB: {e}")
            return 0

    async def get_all_users(self):
        """Get list of all user IDs"""
        try:
            if not await self._check_connection():
                return []
            users = []
            # Use projection to only fetch IDs for speed
            async for user in self.col.find({}, {'id': 1, '_id': 0}):
                users.append(user['id'])
            return users
        except Exception as e:
            logger.error(f"Error getting all users from MongoDB: {e}")
            return []

    async def delete_user(self, user_id):
        try:
            if not await self._check_connection():
                return False
            await self.col.delete_many({'id': int(user_id)})
            return True
        except Exception as e:
            logger.error(f"Error deleting user from MongoDB: {e}")
            return False

db = None
if Config.DATABASE_URL:
    try:
        db = Database(Config.DATABASE_URL, "TelegramStreamBot")
        logger.info("MongoDB client initialized (connection will be verified on first use)")
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB: {e}")
        logger.warning("Falling back to JSON file storage")
        db = None
else:
    logger.warning("DATABASE_URL not found! Using JSON file storage (not recommended for production)")
