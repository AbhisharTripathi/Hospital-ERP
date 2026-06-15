
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
from app.core.config import settings


client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

async def connect_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    
    
    await db.patients.create_index("patient_id", unique=True)
    print("mongodb is successfully connected and indexs are ready")
    

async def close_mongo():
    global client
    if client:
        client.close()
        print("mongodb connection close securely")


def get_db():
    return db