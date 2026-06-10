from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .api.v1.patient import router as patient_router
MONGO_DETAILS = "mongodb://localhost:27017"
client: AsyncIOMotorClient = None

async def connect_mongo():
    global client
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_DETAILS)
    # Aapka database naam jo bhi ho, jaise 'hospital_db'
    return client.hospital_db

async def close_mongo():
    global client
    if client:
        print("Closing MongoDB connection...")
        client.close()
def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.db = await connect_mongo()
        yield
        await close_mongo()

    app = FastAPI(lifespan=lifespan)

    
    app.include_router(patient_router,prefix="/patients")

    return app
