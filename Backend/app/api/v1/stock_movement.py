from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_stock_movement_service,
    require_role
)

from app.models.user import UserRole

from app.models.stock_movement import (
    StockMovementType
)

from app.schemas.stock_movement import (
    StockMovementCreate
)


router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movement"]
)


# ==========================================
# Create Movement
# ==========================================

@router.post("")
async def create_movement(

    movement_data: StockMovementCreate,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    movement_service=Depends(
        get_stock_movement_service
    )

):

    return await movement_service.create_movement(

        current_user=current_user,

        movement_data=movement_data

    )


# ==========================================
# Get All Movements
# ==========================================

@router.get("")
async def get_all_movements(

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    stock_id: str | None = Query(
        default=None
    ),

    medicine_id: str | None = Query(
        default=None
    ),

    batch_id: str | None = Query(
        default=None
    ),

    movement_type: StockMovementType | None = Query(
        default=None
    ),

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    movement_service=Depends(
        get_stock_movement_service
    )

):

    return await movement_service.get_all_movements(

        current_user=current_user,

        page=page,

        limit=limit,

        stock_id=stock_id,

        medicine_id=medicine_id,

        batch_id=batch_id,

        movement_type=movement_type

    )


# ==========================================
# Get Stock History
# ==========================================

@router.get("/stock/{stock_id}")
async def get_stock_history(

    stock_id: str,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    movement_service=Depends(
        get_stock_movement_service
    )

):

    return await movement_service.get_stock_history(

        current_user=current_user,

        stock_id=stock_id

    )


# ==========================================
# Get By Reference
# ==========================================

@router.get("/reference/{reference_type}/{reference_id}")
async def get_by_reference(

    reference_type: str,

    reference_id: str,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    movement_service=Depends(
        get_stock_movement_service
    )

):

    return await movement_service.get_by_reference(

        current_user=current_user,

        reference_type=reference_type,

        reference_id=reference_id

    )


# ==========================================
# Get Movement By ID
# ==========================================

@router.get("/{movement_id}")
async def get_movement_by_id(

    movement_id: str,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    movement_service=Depends(
        get_stock_movement_service
    )

):

    return await movement_service.get_movement_by_id(

        current_user=current_user,

        movement_id=movement_id

    )