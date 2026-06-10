from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.v1.patient import router as patient_router


from .core.database import connect_mongo, close_mongo


def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.db = await connect_mongo()
        yield
        await close_mongo()

    app = FastAPI(lifespan=lifespan)

    
    app.include_router(patient_router,prefix="/patients")

    return app
        close_mongo()

  
