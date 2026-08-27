from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_purchase_service,
    require_role
)

from app.models.user import UserRole

from app.models.purchase import (
    PurchaseStatus
)

from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseUpdate,
    PurchaseStatusUpdate
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


# ==========================================
# Create Purchase
# ==========================================

@router.post("")
async def create_purchase(

    purchase_data: PurchaseCreate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.create_purchase(

        current_user=current_user,

        purchase_data=purchase_data

    )


# ==========================================
# Get All Purchases
# ==========================================

@router.get("")
async def get_all_purchases(

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

    supplier_id: str | None = None,

    status: PurchaseStatus | None = None,

    sort_by: str = "created_at",

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

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.get_all_purchases(

        current_user=current_user,

        page=page,

        limit=limit,

        search=search,

        supplier_id=supplier_id,

        status=status,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Get Purchase By ID
# ==========================================

@router.get("/{purchase_id}")
async def get_purchase_by_id(

    purchase_id: str,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.get_purchase_by_id(

        current_user=current_user,

        purchase_id=purchase_id

    )


# ==========================================
# Get Supplier Purchase History
# ==========================================

@router.get("/supplier/{supplier_id}")
async def get_supplier_purchases(

    supplier_id: str,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.get_supplier_purchases(

        current_user=current_user,

        supplier_id=supplier_id

    )


# ==========================================
# Update Purchase
# ==========================================

@router.put("/{purchase_id}")
async def update_purchase(

    purchase_id: str,

    purchase_data: PurchaseUpdate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.update_purchase(

        current_user=current_user,

        purchase_id=purchase_id,

        purchase_data=purchase_data

    )


# ==========================================
# Update Purchase Status
# ==========================================

@router.patch("/{purchase_id}/status")
async def update_purchase_status(

    purchase_id: str,

    status_data: PurchaseStatusUpdate,

    current_user=Depends(

        require_role(

            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.update_status(

        current_user=current_user,

        purchase_id=purchase_id,

        purchase_status=status_data.status

    )


# ==========================================
# Delete Purchase
# ==========================================

@router.delete("/{purchase_id}")
async def delete_purchase(

    purchase_id: str,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,
            UserRole.SUPER_ADMIN

        )

    ),

    purchase_service=Depends(
        get_purchase_service
    )

):

    return await purchase_service.delete_purchase(

        current_user=current_user,

        purchase_id=purchase_id

    )