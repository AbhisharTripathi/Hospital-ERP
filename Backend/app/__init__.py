from fastapi import FastAPI
from .core.database import connect_mongo, close_mongo, init_indexes
from contextlib import asynccontextmanager

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