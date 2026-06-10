from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

def connect_mongo():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    print("Connected with Database...")
    return client, db

def close_mongo(client):
    if client:
        client.close()

async def init_indexes(db):
    await db.patients.create_index("patient_id", unique=True)