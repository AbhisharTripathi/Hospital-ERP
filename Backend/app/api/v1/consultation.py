from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_consultation_service,
    require_role
)

from app.models.user import UserRole

from app.models.consultation import (
    ConsultationStatus
)

from app.schemas.consultation import (
    ConsultationCreate,
    ConsultationUpdate,
    ConsultationStatusUpdate
)

router = APIRouter(
    prefix="/consultations",
    tags=["Consultation"]
)


# ==========================================
# Create Consultation
# ==========================================

@router.post("")

async def create_consultation(

    consultation_data: ConsultationCreate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.create_consultation(

        hospital_id=current_user["hospital_id"],

        current_user=current_user,

        consultation_data=consultation_data

    )


# ==========================================
# Get Consultation By ID
# ==========================================

@router.get("/{consultation_id}")

async def get_consultation_by_id(

    consultation_id: str,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.get_by_consultation_id(

        hospital_id=current_user["hospital_id"],

        consultation_id=consultation_id

    )


# ==========================================
# Get Patient Consultation History
# ==========================================

@router.get("/patient/{patient_id}")

async def get_patient_consultations(

    patient_id: str,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.get_patient_consultations(

        hospital_id=current_user["hospital_id"],

        patient_id=patient_id

    )


# ==========================================
# Get All Consultations
# ==========================================

@router.get("")

async def get_all_consultations(

    page: int = 1,

    limit: int = 20,

    search: str | None = None,

    doctor_id: str | None = None,

    patient_id: str | None = None,

    status: ConsultationStatus | None = Query(
        default=None
    ),

    sort_by: str = "created_at",

    sort_order: int = -1,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.get_all_consultations(

        hospital_id=current_user["hospital_id"],

        page=page,

        limit=limit,

        search=search,

        doctor_id=doctor_id,

        patient_id=patient_id,

        status=status,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Update Consultation
# ==========================================

@router.put("/{consultation_id}")

async def update_consultation(

    consultation_id: str,

    consultation_data: ConsultationUpdate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.update_consultation(

        hospital_id=current_user["hospital_id"],

        consultation_id=consultation_id,

        consultation_data=consultation_data

    )


# ==========================================
# Update Status
# ==========================================

@router.patch("/{consultation_id}/status")

async def update_consultation_status(

    consultation_id: str,

    status_data: ConsultationStatusUpdate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.update_status(

        hospital_id=current_user["hospital_id"],

        consultation_id=consultation_id,

        status_data=status_data

    )


# ==========================================
# Delete Consultation
# ==========================================

@router.delete("/{consultation_id}")

async def delete_consultation(

    consultation_id: str,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    consultation_service=Depends(
        get_consultation_service
    )

):

    return await consultation_service.delete_consultation(

        hospital_id=current_user["hospital_id"],

        consultation_id=consultation_id

    )