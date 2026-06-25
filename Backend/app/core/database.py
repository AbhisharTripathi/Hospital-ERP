
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
from app.core.config import settings # iska kaam hai database ka Url(mongo_uri) aur database ka naam laakar dena



client: AsyncIOMotorClient | None = None # database ka rasta hai clint
db: AsyncIOMotorDatabase | None = None # actual database

async def connect_mongo():
    global client, db # inhe globally share kiya jayega
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
    return db # jab service ya repository ko databsdedd se koi kaam ho to wo db ko get db se hi lega