from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_patient_services
from app.services.patient import PatientServices
from app.schemas.patient import PatientCreate

router = APIRouter(prefix="/patient", tags=["patient"])

@router.post("")
async def create_patient(
    patient : PatientCreate,
    patient_services : PatientServices = Depends(get_patient_services)
):
    result = await patient_services.create_patient(patient)
    return {"id": result}