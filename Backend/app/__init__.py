# from fastapi import FastAPI
# from .core.database import connect_mongo, close_mongo, init_indexes
# from contextlib import asynccontextmanager

# def create_app():

#     @asynccontextmanager
#     async def lifespan(app: FastAPI):
#         client, db = connect_mongo()
#         app.state.client = client
#         app.state.db = db
#         await init_indexes(app.state.db)
#         yield
#         close_mongo(app.state.client)

#     app = FastAPI(lifespan=lifespan)

#     from .api.v1 import patient_router
#     app.include_router(patient_router)

#     return app
# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from .core.database import (
#     connect_mongo,
#     close_mongo,
#     db
# )

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .core import database
from .api.v1.patient import router as patient_router
from .api.v1.auth import router as auth_router


def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        await database.connect_mongo()

        app.state.db = database.db

        yield

        await database.close_mongo()

    app = FastAPI(
        title="Hospital ERP",
        lifespan=lifespan
    )

   

    app.include_router(patient_router)
    app.include_router(auth_router)

    return app
