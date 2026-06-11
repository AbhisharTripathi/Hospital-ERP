from fastapi import APIRouter,  Depends, Request
from app.dependencies import get_patient_services
from app.services.patient import PatientServices
from app.schemas.patient import PatientCreate, PatientResponse

# from fastapi.responses import HTMLResponse
# from app.core.templates import templates

router = APIRouter(prefix="/patient", tags=["patient"])

@router.post("", response_model=PatientResponse)
async def create_patient(
    patient : PatientCreate,
    patient_services : PatientServices = Depends(get_patient_services)
):
    inserted_id = await patient_services.create_patient(patient)
    patient_data = await patient_services.get_patient_data(inserted_id)
    print(patient_data)
    return {
        "message": "Patient created successfully",
        "id": str(inserted_id)
    }

# @router.get("/form", response_class=HTMLResponse)
# async def patient_form(request: Request):
#     return templates.TemplateResponse(
#         "patient_form.html",
#         {"request": request}
#     )
