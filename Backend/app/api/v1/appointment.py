from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from app.dependencies import (
    get_appointment_service,
    require_role
)

from app.models.user import UserRole

from app.models.appointment import (
    AppointmentStatus
)

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentStatusUpdate
)

from app.services.appointment import (
    AppointmentService
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# -------------------------------------------------------
# Create Appointment
# -------------------------------------------------------

@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_appointment(

    appointment_data: AppointmentCreate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST
        )
    ),

    appointment_service: AppointmentService = Depends(
        get_appointment_service
    )

):

    return await appointment_service.create_appointment(

        current_user=current_user,

        appointment_data=appointment_data

    )


# -------------------------------------------------------
# Get All Appointments
# -------------------------------------------------------

@router.get(
    ""
)
async def get_all_appointments(

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    search: str | None = None,

    doctor_id: str | None = None,

    patient_id: str | None = None,

    status_filter: AppointmentStatus | None = Query(
        default=None,
        alias="status"
    ),

    appointment_date: date | None = None,

    sort_by: str = "appointment_date",

    sort_order: int = -1,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR
        )
    ),

    appointment_service: AppointmentService = Depends(
        get_appointment_service
    )

):

    return await appointment_service.get_all_appointments(

        current_user=current_user,

        page=page,

        limit=limit,

        search=search,

        doctor_id=doctor_id,

        patient_id=patient_id,

        status=status_filter,

        appointment_date=appointment_date,

        sort_by=sort_by,

        sort_order=sort_order

    )


# -------------------------------------------------------
# Get Appointment By ID
# -------------------------------------------------------

@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
async def get_appointment_by_id(

    appointment_id: str,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR
        )
    ),

    appointment_service: AppointmentService = Depends(
        get_appointment_service
    )

):

    return await appointment_service.get_appointment_by_id(

        current_user=current_user,

        appointment_id=appointment_id

    )


# -------------------------------------------------------
# Update Appointment
# -------------------------------------------------------

@router.patch(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
async def update_appointment(

    appointment_id: str,

    appointment_data: AppointmentUpdate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST
        )
    ),

    appointment_service: AppointmentService = Depends(
        get_appointment_service
    )

):

    return await appointment_service.update_appointment(

        current_user=current_user,

        appointment_id=appointment_id,

        appointment_data=appointment_data

    )


# -------------------------------------------------------
# Update Appointment Status
# -------------------------------------------------------

@router.patch(
    "/{appointment_id}/status",
    response_model=AppointmentResponse
)
async def update_status(

    appointment_id: str,

    status_data: AppointmentStatusUpdate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR
        )
    ),

    appointment_service: AppointmentService = Depends(
        get_appointment_service
    )

):

    return await appointment_service.update_status(

        current_user=current_user,

        appointment_id=appointment_id,

        status_data=status_data

    )


# -------------------------------------------------------
# Delete Appointment
# -------------------------------------------------------

@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_200_OK
)
async def delete_appointment(

    appointment_id: str,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    appointment_service: AppointmentService = Depends(
        get_appointment_service
    )

):

    return await appointment_service.delete_appointment(

        current_user=current_user,

        appointment_id=appointment_id

    )