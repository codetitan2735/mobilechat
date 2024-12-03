from motor.motor_asyncio import AsyncIOMotorClient

from settings import MONGODB_URL

mongodb_client = AsyncIOMotorClient(MONGODB_URL)
mongo_chat_db = mongodb_client.chat
