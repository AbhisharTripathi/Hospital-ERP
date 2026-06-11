from fastapi import FastAPI
from .core.database import connect_mongo, close_mongo, init_indexes
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
        client, db = connect_mongo()
        app.state.client = client
        app.state.db = db
        await init_indexes(app.state.db)
        yield
        close_mongo(app.state.client)

    app = FastAPI(lifespan=lifespan)

    from .api.v1 import patient_router
    app.include_router(patient_router)

    return app
