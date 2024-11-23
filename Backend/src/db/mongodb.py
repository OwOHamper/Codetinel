from motor.motor_asyncio import AsyncIOMotorClient
from src.config import get_settings

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def get_database():
    return db.client["aipentester"]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)

async def close_mongo_connection():
    db.client.close() 