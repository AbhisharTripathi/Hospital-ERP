from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_batch_service,
    require_role
)

from app.models.user import UserRole

from app.models.batch import (
    BatchStatus
)

from app.schemas.batch import (
    BatchCreate,
    BatchUpdate
)
from datetime import date


router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)


# ==========================================
# Create Batch
# ==========================================

@router.post("")
async def create_batch(

    batch_data: BatchCreate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    batch_service=Depends(
        get_batch_service
    )

):

    return await batch_service.create_batch(

        current_user=current_user,

        batch_data=batch_data

    )


# ==========================================
# Get All Batches
# ==========================================

@router.get("")
async def get_all_batches(

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    medicine_id: str | None = Query(
        default=None
    ),

    status: BatchStatus | None = Query(
        default=None
    ),

    sort_by: str = Query(
        default="expiry_date"
    ),

    sort_order: int = Query(
        default=1,
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

    batch_service=Depends(
        get_batch_service
    )

):

    return await batch_service.get_all_batches(

        current_user=current_user,

        page=page,

        limit=limit,

        medicine_id=medicine_id,

        status=status,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Get Batches By Medicine
# ==========================================

@router.get("/medicine/{medicine_id}")
async def get_batches_by_medicine(

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

    batch_service=Depends(
        get_batch_service
    )

):

    return await batch_service.get_batches_by_medicine(

        current_user=current_user,

        medicine_id=medicine_id

    )


# ==========================================
# Get Expired Batches
# ==========================================

@router.get("/expired")
async def get_expired_batches(

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    batch_service=Depends(
        get_batch_service
    )

):

    

    return await batch_service.get_expired_batches(

        current_user=current_user,

        today=date.today()

    )


# ==========================================
# Get Batch By ID
# ==========================================

@router.get("/{batch_id}")
async def get_batch_by_id(

    batch_id: str,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST

        )

    ),

    batch_service=Depends(
        get_batch_service
    )

):

    return await batch_service.get_batch_by_id(

        current_user=current_user,

        batch_id=batch_id

    )


# ==========================================
# Update Batch
# ==========================================

@router.put("/{batch_id}")
async def update_batch(

    batch_id: str,

    batch_data: BatchUpdate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    batch_service=Depends(
        get_batch_service
    )

):

    return await batch_service.update_batch(

        current_user=current_user,

        batch_id=batch_id,

        batch_data=batch_data

    )