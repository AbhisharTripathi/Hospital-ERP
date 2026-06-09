from fastapi import Request, Depends
from .repositories.patient import PatientRepository

def get_db(request : Request):
    return request.app.state.db

def get_patient_repository(db = Depends(get_db)):
    return PatientRepository(db)