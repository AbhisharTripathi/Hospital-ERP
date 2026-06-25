
from fastapi import APIRouter, Depends, Request,HTTPException, status
from app.dependencies import get_patient_services
from app.services.patient import PatientServices
from app.schemas.patient import (
    PatientCreate,
    PatientResponse,
    PatientUpdate
)

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    patient_services: PatientServices = Depends(get_patient_services)
):
    try:
        result = await patient_services.create_patient(patient)
        
        # Bug Fix: Fetch by custom patient_id instead of inserted_id (ObjectId)
        patient_data = await patient_services.get_patient_by_id(result["patient_id"])

        return patient_data
    except HTTPException as http_exc:
        # for duplicate phone number
        raise http_exc
    except Exception as e:
        #baaki sabhi error ke liye
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server  error : {str(e)}"
        )

@router.get("", response_model=list[PatientResponse])
async def get_all_patients(
    limit: int = 100,
    patient_services: PatientServices = Depends(get_patient_services)
):
    return await patient_services.get_all_patients(limit)

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient_by_id(
    patient_id: str,
    patient_services: PatientServices = Depends(get_patient_services)
):
    # Method name is now consistent
    return await patient_services.get_patient_by_id(patient_id)

@router.put("/{patient_id}")
async def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    patient_services: PatientServices = Depends(get_patient_services)
):
    return await patient_services.update_patient(patient_id, patient_update)

@router.patch("/{patient_id}/deactivate")
async def deactivate_patient(
    patient_id: str,
    patient_services: PatientServices = Depends(get_patient_services)
):
    return await patient_services.deactivate_patient(patient_id)