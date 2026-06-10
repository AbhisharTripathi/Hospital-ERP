from fastapi import FastAPI
from .core.database import connect_mongo, close_mongo
from contextlib import asynccontextmanager

def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.db = await connect_mongo()
        yield
        await close_mongo()

    app = FastAPI(lifespan=lifespan)

    from .api.v1 import patient_router
    app.include_router(patient_router)

    return app