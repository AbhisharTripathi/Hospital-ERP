from pymongo import AsyncMongoClient
from .config import settings

client = None

async def connect_mongo():
    global client
    client = AsyncMongoClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    print("Connected with Database...")
    return db

async def close_mongo():
    global client
    if client:
        client.close()