from fastapi import (
    APIRouter,
    Depends
)

from app.dependencies import (
    get_doctor_service,
    require_role
)

from app.models.user import UserRole

from app.services.doctor import DoctorService

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)
@router.post(
    "",
    response_model=dict
)
async def create_doctor(
    doctor: DoctorCreate,
    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),
    current_user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await doctor_service.create_doctor(
        doctor
    )
@router.get(
    "",
    response_model=list[DoctorResponse]
)
async def get_all_doctors(
    doctor_service: DoctorService = Depends(
        get_doctor_service
    )
):

    return await doctor_service.get_all_doctors()
@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
async def get_doctor_by_id(
    doctor_id: str,
    doctor_service: DoctorService = Depends(
        get_doctor_service
    )
):

    return await doctor_service.get_doctor_by_id(
        doctor_id
    )
@router.put(
    "/{doctor_id}"
)
async def update_doctor(
    doctor_id: str,
    doctor_update: DoctorUpdate,
    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),
    current_user=Depends(
        require_role(
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.update_doctor(
        doctor_id,
        doctor_update
    )
@router.patch(
    "/{doctor_id}/deactivate"
)
async def deactivate_doctor(
    doctor_id: str,
    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),
    current_user=Depends(
        require_role(
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.deactivate_doctor(
        doctor_id
    )