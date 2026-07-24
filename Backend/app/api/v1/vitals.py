from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_current_user,
    get_vital_service,
    require_role
)

from app.models.user import UserRole
from app.models.vitals import VitalStatus

from app.schemas.pagination import (
    PaginatedResponse
)

from app.schemas.vitals import (
    VitalCreate,
    VitalUpdate,
    VitalStatusUpdate,
    VitalResponse
)

router = APIRouter(

    prefix="/vitals",

    tags=["Vitals"]

)


# ==========================================
# Create Vital
# ==========================================

@router.post(

    "",

    response_model=dict

)

async def create_vital(

    vital_data: VitalCreate,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            # UserRole.SUPER_ADMIN,

            UserRole.DOCTOR,

            UserRole.NURSE

        )

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.create_vital(

        hospital_id=current_user["hospital_id"],

        current_user=current_user,

        vital_data=vital_data

    )


# ==========================================
# Get By Vital ID
# ==========================================

@router.get(

    "/{vital_id}",

    response_model=VitalResponse

)

async def get_vital(

    vital_id: str,

    current_user=Depends(

        get_current_user

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.get_by_vital_id(

        current_user["hospital_id"],

        vital_id

    )


# ==========================================
# Patient Vital History
# ==========================================

@router.get(

    "/patient/{patient_id}",

    response_model=list[VitalResponse]

)

async def get_patient_vitals(

    patient_id: str,

    current_user=Depends(

        get_current_user

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.get_patient_vitals(

        current_user["hospital_id"],

        patient_id

    )


# ==========================================
# Get All Vitals
# ==========================================

@router.get(

    "",

    response_model=PaginatedResponse[VitalResponse]

)

async def get_all_vitals(

    page: int = Query(

        default=1,

        ge=1

    ),

    limit: int = Query(

        default=10,

        ge=1,

        le=100

    ),

    search: str | None = None,

    doctor_id: str | None = None,

    patient_id: str | None = None,

    status: VitalStatus | None = None,

    current_user=Depends(

        get_current_user

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.get_all_vitals(

        hospital_id=current_user["hospital_id"],

        page=page,

        limit=limit,

        search=search,

        doctor_id=doctor_id,

        patient_id=patient_id,

        status=status

    )


# ==========================================
# Update Vital
# ==========================================

@router.put(

    "/{vital_id}",

    response_model=dict

)

async def update_vital(

    vital_id: str,

    update_data: VitalUpdate,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            # UserRole.SUPER_ADMIN,
            UserRole.DOCTOR,

            UserRole.NURSE

        )

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.update_vital(

        hospital_id=current_user["hospital_id"],

        vital_id=vital_id,

        update_data=update_data

    )


# ==========================================
# Update Status
# ==========================================

@router.patch(

    "/{vital_id}/status",

    response_model=dict

)

async def update_status(

    vital_id: str,

    status_data: VitalStatusUpdate,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            # UserRole.SUPER_ADMIN,
            UserRole.DOCTOR

        )

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.update_status(

        hospital_id=current_user["hospital_id"],

        vital_id=vital_id,

        status_data=status_data

    )


# ==========================================
# Delete Vital
# ==========================================

@router.delete(

    "/{vital_id}",

    response_model=dict

)

async def delete_vital(

    vital_id: str,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            # UserRole.SUPER_ADMIN

        )

    ),

    vital_service=Depends(

        get_vital_service

    )

):

    return await vital_service.delete_vital(

        hospital_id=current_user["hospital_id"],

        vital_id=vital_id

    )

