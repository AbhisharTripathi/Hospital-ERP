from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.dependencies import (
    get_doctor_service,
    require_role
)

from app.models.user import UserRole

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    UpdateDoctorStatus
)

from app.services.doctor import DoctorService


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# -------------------- Create Doctor Profile -------------------- #

@router.post(
    "/profile",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_doctor_profile(
    doctor_data: DoctorCreate,
    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),
    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.create_doctor_profile(
        doctor_data=doctor_data,
        current_user=current_user
    )


# -------------------- Get All Doctors -------------------- #

@router.get(
    "",
    response_model=list[DoctorResponse]
    
)
async def get_all_doctors(

    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.get_all_doctors(
        current_user=current_user
    )



# -------------------- Get Doctor By department ID -------------------- #

@router.get(
    "/department/{department_id}",
    response_model=list[DoctorResponse]
)
async def get_doctors_by_department(

    department_id: str,

    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.get_doctors_by_department(

        current_user=current_user,

        department_id=department_id
    )

# -------------------- Get Doctor By ID -------------------- #

@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse,
    
)
async def get_doctor_by_id(

    doctor_id: str,

    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.get_doctor_by_id(
        current_user=current_user,
        doctor_id=doctor_id
    )


# -------------------- Update Doctor -------------------- #

@router.patch(
    "/{doctor_id}",
    response_model=DoctorResponse,
    status_code=status.HTTP_200_OK
)
async def update_doctor(

    doctor_id: str,

    doctor_data: DoctorUpdate,

    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.update_doctor(
        current_user=current_user,
        doctor_id=doctor_id,
        doctor_data=doctor_data
    )


# -------------------- Update Doctor Status -------------------- #

@router.patch(
    "/{doctor_id}/status",
    response_model=DoctorResponse,
    status_code=status.HTTP_200_OK
)
async def update_doctor_status(

    doctor_id: str,

    status_data: UpdateDoctorStatus,

    doctor_service: DoctorService = Depends(
        get_doctor_service
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )
):

    return await doctor_service.update_doctor_status(

        current_user=current_user,

        doctor_id=doctor_id,

        status_data=status_data
    )