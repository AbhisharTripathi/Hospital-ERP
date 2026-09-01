from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_stock_service,
    require_role
)

from app.models.user import UserRole

from app.models.stock import (
    StockStatus
)

from app.schemas.stock import (
    StockCreate,
    StockUpdate
)


router = APIRouter(
    prefix="/stocks",
    tags=["Stock"]
)


# ==========================================
# Create Stock
# ==========================================

@router.post("")
async def create_stock(

    stock_data: StockCreate,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    stock_service=Depends(
        get_stock_service
    )

):

    return await stock_service.create_stock(

        current_user=current_user,

        stock_data=stock_data

    )


# ==========================================
# Get All Stock
# ==========================================

@router.get("")
async def get_all_stock(

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

    batch_id: str | None = Query(
        default=None
    ),

    status: StockStatus | None = Query(
        default=None
    ),

    sort_by: str = Query(
        default="updated_at"
    ),

    sort_order: int = Query(
        default=-1,
        ge=-1,
        le=1
    ),

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    stock_service=Depends(
        get_stock_service
    )

):

    return await stock_service.get_all_stock(

        current_user=current_user,

        page=page,

        limit=limit,

        medicine_id=medicine_id,

        batch_id=batch_id,

        status=status,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Get Stock By Medicine
# ==========================================

@router.get("/medicine/{medicine_id}")
async def get_medicine_stock(

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

    stock_service=Depends(
        get_stock_service
    )

):

    return await stock_service.get_medicine_stock(

        current_user=current_user,

        medicine_id=medicine_id

    )


# ==========================================
# Get Stock By ID
# ==========================================

@router.get("/{stock_id}")
async def get_stock_by_id(

    stock_id: str,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    stock_service=Depends(
        get_stock_service
    )

):

    return await stock_service.get_stock_by_id(

        current_user=current_user,

        stock_id=stock_id

    )


# ==========================================
# Update Stock
# ==========================================

@router.patch("/{stock_id}")
async def update_stock(

    stock_id: str,

    stock_data: StockUpdate,

    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),

    stock_service=Depends(
        get_stock_service
    )

):

    return await stock_service.update_stock(

        current_user=current_user,

        stock_id=stock_id,

        stock_data=stock_data

    )