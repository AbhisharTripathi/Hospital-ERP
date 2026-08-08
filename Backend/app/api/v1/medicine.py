from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_medicine_service,
    require_role
)

from app.models.user import UserRole

from app.models.medicine import (
    DosageForm
)

from app.schemas.medicine import (
    MedicineCreate,
    MedicineUpdate
)


router = APIRouter(
    prefix="/medicines",
    tags=["Medicines"]
)


# ==========================================
# Create Medicine
# ==========================================

@router.post("")
async def create_medicine(

    medicine_data: MedicineCreate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    medicine_service=Depends(
        get_medicine_service
    )

):

    return await medicine_service.create_medicine(

        hospital_id=current_user["hospital_id"],

        medicine_data=medicine_data,

        current_user=current_user

    )


# ==========================================
# Search / Autocomplete
# ==========================================

@router.get("/search")
async def search_medicines(

    q: str = Query(
        min_length=2,
        max_length=100
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=20
    ),

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    medicine_service=Depends(
        get_medicine_service
    )

):

    return await medicine_service.search_medicines(

        hospital_id=current_user["hospital_id"],

        search=q,

        limit=limit

    )


# ==========================================
# Get All Medicines
# ==========================================

@router.get("")
async def get_all_medicines(

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    search: str | None = Query(
        default=None,
        max_length=100
    ),

    dosage_form: DosageForm | None = None,

    manufacturer: str | None = Query(
        default=None,
        max_length=150
    ),

    is_active: bool | None = None,

    sort_by: str = "created_at",

    sort_order: int = Query(
        default=-1,
        ge=-1,
        le=1
    ),

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    medicine_service=Depends(
        get_medicine_service
    )

):

    return await medicine_service.get_all_medicines(

        hospital_id=current_user["hospital_id"],

        page=page,

        limit=limit,

        search=search,

        dosage_form=dosage_form,

        manufacturer=manufacturer,

        is_active=is_active,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Get Medicine By ID
# ==========================================

@router.get("/{medicine_id}")
async def get_medicine_by_id(

    medicine_id: str,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    medicine_service=Depends(
        get_medicine_service
    )

):

    return await medicine_service.get_by_medicine_id(

        hospital_id=current_user["hospital_id"],

        medicine_id=medicine_id

    )


# ==========================================
# Update Medicine
# ==========================================

@router.put("/{medicine_id}")
async def update_medicine(

    medicine_id: str,

    medicine_data: MedicineUpdate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    medicine_service=Depends(
        get_medicine_service
    )

):

    return await medicine_service.update_medicine(

        hospital_id=current_user["hospital_id"],

        medicine_id=medicine_id,

        medicine_data=medicine_data

    )


# ==========================================
# Activate / Deactivate
# ==========================================

@router.patch("/{medicine_id}/status")
async def update_medicine_status(

    medicine_id: str,

    is_active: bool,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    medicine_service=Depends(
        get_medicine_service
    )

):

    return await medicine_service.update_status(

        hospital_id=current_user["hospital_id"],

        medicine_id=medicine_id,

        is_active=is_active

    )