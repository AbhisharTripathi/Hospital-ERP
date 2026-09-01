# from fastapi import(
#     APIRouter,
#     Depends,
#     Query
# )
# from app.dependencies import(
#     get_supplier_service,
#     require_role
# )

# from app.models.user import UserRole

# from app.schemas.supplier import(
#     SupplierCreate,
#     SupplierUpdate
# )

# router = APIRouter(
#     prefix="/suppliers",
#     tags=["suppliers"]
# )

# # --------Create Supplier------------

# @router.post("")
# async def create_supplier(
#     supplier_data:SupplierCreate,
#     current_user=Depends(
#         require_role(
#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN
#         )
#     ),
#     supplier_service=Depends(
#         get_supplier_service
#     )
# ):
#     return await supplier_service.create_supplier(
#         current_user=current_user,
#         supplier_data=supplier_data
#     )


# #----------- search/Autocomplete------------

# async def search_suppliers(
#         q: str=Query(
#             min_length=2,
#             max_length=100

#         ),
#         limit:int=Query(
#             default=10,
#             ge=1,
#             le=20
#         ),
#         current_user=Depends(
#             require_role(
#                 UserRole.PHARMACIST,
#                 UserRole.ADMIN,
#                 UserRole.SUPER_ADMIN,
#                 UserRole.RECEPTIONIST
#             )
#         ),
#         supplier_service=Depends(
#             get_supplier_service
#         )

# ):
#     return await supplier_service.search_suppliers(
#         current_user=current_user,
#         search=q,
#         limit=limit
#     )


# # ==========================================
# # Get All Suppliers
# # ==========================================

# @router.get("")
# async def get_all_suppliers(

#     page: int = Query(
#         default=1,
#         ge=1
#     ),

#     limit: int = Query(
#         default=20,
#         ge=1,
#         le=100
#     ),

#     search: str | None = Query(
#         default=None,
#         max_length=100
#     ),

#     is_active: bool | None = None,

#     sort_by: str = "created_at",

#     sort_order: int = Query(
#         default=-1,
#         ge=-1,
#         le=1
#     ),

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN,
#             UserRole.RECEPTIONIST

#         )

#     ),

#     supplier_service=Depends(
#         get_supplier_service
#     )

# ):

#     return await supplier_service.get_all_suppliers(

#         current_user=current_user,

#         page=page,

#         limit=limit,

#         search=search,

#         is_active=is_active,

#         sort_by=sort_by,

#         sort_order=sort_order

#     )


# # ==========================================
# # Get Supplier By ID
# # ==========================================

# @router.get("/{supplier_id}")
# async def get_supplier_by_id(

#     supplier_id: str,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN,
#             UserRole.RECEPTIONIST

#         )

#     ),

#     supplier_service=Depends(
#         get_supplier_service
#     )

# ):

#     return await supplier_service.get_supplier_by_id(

#         current_user=current_user,

#         supplier_id=supplier_id

#     )


# # ==========================================
# # Update Supplier
# # ==========================================

# @router.put("/{supplier_id}")
# async def update_supplier(

#     supplier_id: str,

#     supplier_data: SupplierUpdate,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     supplier_service=Depends(
#         get_supplier_service
#     )

# ):

#     return await supplier_service.update_supplier(

#         current_user=current_user,

#         supplier_id=supplier_id,

#         supplier_data=supplier_data

#     )


# # ==========================================
# # Activate / Deactivate
# # ==========================================

# @router.patch("/{supplier_id}/status")
# async def update_supplier_status(

#     supplier_id: str,

#     is_active: bool,

#     current_user=Depends(

#         require_role(

#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     supplier_service=Depends(
#         get_supplier_service
#     )

# ):

#     return await supplier_service.update_status(

#         current_user=current_user,

#         supplier_id=supplier_id,

#         is_active=is_active

#     )


# # ==========================================
# # Delete Supplier
# # ==========================================

# @router.delete("/{supplier_id}")
# async def delete_supplier(

#     supplier_id: str,

#     current_user=Depends(

#         require_role(

#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     supplier_service=Depends(
#         get_supplier_service
#     )

# ):

#     return await supplier_service.delete_supplier(

#         current_user=current_user,

#         supplier_id=supplier_id

#     )


from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from app.dependencies import (
    get_supplier_service,
    require_role
)
from app.models.user import UserRole
from app.schemas.pagination import PaginatedResponse
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate
)
from app.services.supplier import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


# -------------------- Create Supplier -------------------- #

@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_supplier(
    supplier_data: SupplierCreate,
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await supplier_service.create_supplier(
        current_user=current_user,
        supplier_data=supplier_data
    )


# -------------------- Search / Autocomplete -------------------- #

@router.get(
    "/search",
    response_model=list[SupplierResponse]
)
async def search_suppliers(
    q: str = Query(
        ...,
        min_length=2,
        max_length=100
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=20
    ),
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST
        )
    )
):
    return await supplier_service.search_suppliers(
        current_user=current_user,
        search=q,
        limit=limit
    )


# -------------------- Get All Suppliers -------------------- #

@router.get(
    "",
    response_model=PaginatedResponse[SupplierResponse]
)
async def get_all_suppliers(
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
    is_active: bool | None = Query(
        default=None
    ),
    sort_by: str = Query(
        default="created_at"
    ),
    sort_order: int = Query(
        default=-1,
        ge=-1,
        le=1
    ),
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST
        )
    )
):
    return await supplier_service.get_all_suppliers(
        current_user=current_user,
        page=page,
        limit=limit,
        search=search,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order
    )


# -------------------- Get Supplier By ID -------------------- #

@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse
)
async def get_supplier_by_id(
    supplier_id: str,
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST
        )
    )
):
    return await supplier_service.get_supplier_by_id(
        current_user=current_user,
        supplier_id=supplier_id
    )


# -------------------- Update Supplier -------------------- #

@router.patch(
    "/{supplier_id}",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK
)
async def update_supplier(
    supplier_id: str,
    supplier_data: SupplierUpdate,
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await supplier_service.update_supplier(
        current_user=current_user,
        supplier_id=supplier_id,
        supplier_data=supplier_data
    )


# -------------------- Activate / Deactivate -------------------- #

@router.patch(
    "/{supplier_id}/status",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK
)
async def update_supplier_status(
    supplier_id: str,
    is_active: bool = Query(...),
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await supplier_service.update_status(
        current_user=current_user,
        supplier_id=supplier_id,
        is_active=is_active
    )


# -------------------- Delete Supplier -------------------- #

@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_200_OK
)
async def delete_supplier(
    supplier_id: str,
    supplier_service: SupplierService = Depends(
        get_supplier_service
    ),
    current_user=Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await supplier_service.delete_supplier(
        current_user=current_user,
        supplier_id=supplier_id
    )