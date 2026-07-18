from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.dependencies import (
    get_doctor_schedule_service,
    require_role
)

from app.models.user import UserRole

from app.schemas.doctor_schedule import (
    DoctorScheduleCreate,
    DoctorScheduleUpdate,
    DoctorScheduleResponse
)

from app.services.doctor_schedule import (
    DoctorScheduleService
)

router = APIRouter(
    prefix="/doctor-schedules",
    tags=["Doctor Schedule"]
)


# -------------------- Create -------------------- #

@router.post(
    "",
    response_model=DoctorScheduleResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_schedule(

    schedule_data: DoctorScheduleCreate,

    schedule_service: DoctorScheduleService = Depends(
        get_doctor_schedule_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await schedule_service.create_schedule(
        current_user=current_user,
        schedule_data=schedule_data
    )


# -------------------- Get Doctor Schedule -------------------- #

@router.get(
    "/doctor/{doctor_id}",
    response_model=list[DoctorScheduleResponse]
)
async def get_doctor_schedule(

    doctor_id: str,

    schedule_service: DoctorScheduleService = Depends(
        get_doctor_schedule_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await schedule_service.get_schedule_by_doctor(
        current_user=current_user,
        doctor_id=doctor_id
    )


# -------------------- Get Schedule By ID -------------------- #

@router.get(
    "/{schedule_id}",
    response_model=DoctorScheduleResponse
)
async def get_schedule_by_id(

    schedule_id: str,

    schedule_service: DoctorScheduleService = Depends(
        get_doctor_schedule_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await schedule_service.get_schedule_by_id(
        current_user=current_user,
        schedule_id=schedule_id
    )


# -------------------- Update -------------------- #

@router.patch(
    "/{schedule_id}",
    response_model=DoctorScheduleResponse
)
async def update_schedule(

    schedule_id: str,

    schedule_data: DoctorScheduleUpdate,

    schedule_service: DoctorScheduleService = Depends(
        get_doctor_schedule_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await schedule_service.update_schedule(
        current_user=current_user,
        schedule_id=schedule_id,
        schedule_data=schedule_data
    )


# -------------------- Status -------------------- #

@router.patch(
    "/{schedule_id}/status",
    response_model=DoctorScheduleResponse
)
async def update_schedule_status(

    schedule_id: str,

    is_active: bool,

    schedule_service: DoctorScheduleService = Depends(
        get_doctor_schedule_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await schedule_service.update_schedule_status(
        current_user=current_user,
        schedule_id=schedule_id,
        is_active=is_active
    )


# -------------------- Delete -------------------- #

@router.delete(
    "/{schedule_id}",
    response_model=dict
)
async def delete_schedule(

    schedule_id: str,

    schedule_service: DoctorScheduleService = Depends(
        get_doctor_schedule_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await schedule_service.delete_schedule(
        current_user=current_user,
        schedule_id=schedule_id
    )