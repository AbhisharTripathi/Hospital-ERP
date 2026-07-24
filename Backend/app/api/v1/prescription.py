from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_prescription_service,
    require_role
)

from app.models.user import UserRole

from app.models.prescription import (
    PrescriptionStatus
)

from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionStatusUpdate
)

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescription"]
)


# ==========================================
# Create Prescription
# ==========================================

@router.post("")

async def create_prescription(

    prescription_data: PrescriptionCreate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.create_prescription(

        hospital_id=current_user["hospital_id"],

        current_user=current_user,

        prescription_data=prescription_data

    )


# ==========================================
# Get Prescription By ID
# ==========================================

@router.get("/{prescription_id}")

async def get_prescription_by_id(

    prescription_id: str,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN,

            UserRole.RECEPTIONIST

        )

    ),

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.get_by_prescription_id(

        hospital_id=current_user["hospital_id"],

        prescription_id=prescription_id

    )


# ==========================================
# Get Patient Prescription History
# ==========================================

@router.get("/patient/{patient_id}")

async def get_patient_prescriptions(

    patient_id: str,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN,

            UserRole.RECEPTIONIST

        )

    ),

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.get_patient_prescriptions(

        hospital_id=current_user["hospital_id"],

        patient_id=patient_id

    )


# ==========================================
# Get All Prescriptions
# ==========================================

@router.get("")

async def get_all_prescriptions(

    page: int = 1,

    limit: int = 20,

    search: str | None = None,

    doctor_id: str | None = None,

    patient_id: str | None = None,

    status: PrescriptionStatus | None = Query(
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

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.get_all_prescriptions(

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
# Update Prescription
# ==========================================

@router.put("/{prescription_id}")

async def update_prescription(

    prescription_id: str,

    prescription_data: PrescriptionUpdate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.update_prescription(

        hospital_id=current_user["hospital_id"],

        prescription_id=prescription_id,

        prescription_data=prescription_data

    )


# ==========================================
# Update Status
# ==========================================

@router.patch("/{prescription_id}/status")

async def update_status(

    prescription_id: str,

    status_data: PrescriptionStatusUpdate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.update_status(

        hospital_id=current_user["hospital_id"],

        prescription_id=prescription_id,

        status_data=status_data

    )


# ==========================================
# Delete Prescription
# ==========================================

@router.delete("/{prescription_id}")

async def delete_prescription(

    prescription_id: str,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    prescription_service=Depends(
        get_prescription_service
    )

):

    return await prescription_service.delete_prescription(

        hospital_id=current_user["hospital_id"],

        prescription_id=prescription_id

    )