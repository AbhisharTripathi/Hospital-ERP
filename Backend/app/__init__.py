from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .core import database
from .api.v1.patient import router as patient_router
from .api.v1.auth import router as auth_router

from .api.v1.doctor import router as doctor_router
from .api.v1.user import router as user_router
from .core.exceptions import register_exception_handlers
import logging
from .api.v1.department import router as department_router
from .api.v1.doctor_schedule import (
    router as doctor_schedule_router
)
from .api.v1.appointment import router as appointment_router

from .api.v1.dashboard import router as dashboard_router

from .api.v1.billing import router as billing_router
from .api.v1.prescription import (router as prescription_router)
from .api.v1.vitals import (router as vital_router)
from .api.v1.consultation import (router as consultation_router)
from app.api.v1.lab_order import (router as lab_order_router)
from app.api.v1.pharmacy import router as pharmacy_router


def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        #jab uvicorn server start karega 
        await database.connect_mongo() 

        app.state.db = database.db #(global) ap poori application me kahi bhi database ko request.app.state.db ke through use kar sakte hai

        yield # yaha app chal rahi hai (request handle ho rahi hai jab tak server chal raha hai)

        await database.close_mongo()#(jab ctrl+c karte hai uvicorn band hota hai to database connection safely band kar diya jaata hai taki dat leak ya crash na ho)

    app = FastAPI(
        title="Hospital ERP",
        lifespan=lifespan # jo decorator hai uske liye lifespan ko function me pass kar diya gaya hai
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    register_exception_handlers(app)

    origins = [
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"], # Allows all headers
    )

   

    app.include_router(patient_router)
    app.include_router(auth_router)
    # app.include_router se hum dono alag alg router ko hum FastAPI app se jod rahe hai 
    
   
    app.include_router(user_router)

    app.include_router(doctor_router)
    app.include_router(department_router)
    app.include_router(doctor_schedule_router)
    app.include_router(appointment_router)
    app.include_router(dashboard_router)
    app.include_router(billing_router)
    app.include_router(prescription_router)
    app.include_router(vital_router)
    app.include_router(consultation_router)
    app.include_router(lab_order_router)
    app.include_router(pharmacy_router)




    return app
