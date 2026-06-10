from fastapi import Request, Depends
from app.repositories.counters import CountersRepository
from app.repositories.patient import PatientRepository
from app.services.patient import PatientServices

def get_db(request : Request):
    return request.app.state.db

def get_counters_repository(db = Depends(get_db)):
    return CountersRepository(db)

def get_patient_repository(db = Depends(get_db)):
    return PatientRepository(db)

def get_patient_services(
        patient_repository : PatientRepository = Depends(get_patient_repository),
        counter_repository : CountersRepository = Depends(get_counters_repository)              
    ):
    return PatientServices(patient_repository, counter_repository)

