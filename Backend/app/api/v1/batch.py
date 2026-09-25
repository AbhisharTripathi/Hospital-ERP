from datetime import date
from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from app.dependencies import (
    get_batch_service,
    require_role
)
from app.models.batch import BatchStatus
from app.models.user import UserRole
from app.schemas.batch import (
    BatchCreate,
    BatchResponse,
    BatchUpdate
)
from app.schemas.pagination import PaginatedResponse
from app.services.batch import BatchService

router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)


# -------------------- Create Batch -------------------- #

@router.post(
    "",
    response_model=BatchResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_batch(
    batch_data: BatchCreate,
    batch_service: BatchService = Depends(
        get_batch_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await batch_service.create_batch(
        current_user=current_user,
        batch_data=batch_data
    )


# -------------------- Get All Batches -------------------- #

# @router.get(
#     "",
#     response_model=PaginatedResponse[BatchResponse]
# )
# async def get_all_batches(
#     page: int = Query(
#         default=1,
#         ge=1
#     ),
#     limit: int = Query(
#         default=20,
#         ge=1,
#         le=100
#     ),
#     medicine_id: str | None = Query(
#         default=None
#     ),
#     status: BatchStatus | None = Query(
#         default=None
#     ),
#     sort_by: str = Query(
#         default="expiry_date"
#     ),
#     sort_order: int = Query(
#         default=1,
#         ge=-1,
#         le=1
#     ),
#     batch_service: BatchService = Depends(
#         get_batch_service
#     ),
#     current_user=Depends(
#         require_role(
#             UserRole.PHARMACIST,
#             UserRole.DOCTOR,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN,
#             UserRole.RECEPTIONIST
#         )
#     )
# ):
#     return await batch_service.get_all_batches(
#         current_user=current_user,
#         page=page,
#         limit=limit,
#         medicine_id=medicine_id,
#         status=status,
#         sort_by=sort_by,
#         sort_order=sort_order
#     )


@router.get("", response_model=PaginatedResponse[BatchResponse])
async def get_all_batches(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    medicine_id: str | None = Query(default=None),
    status: BatchStatus | None = Query(default=None),
    sort_by: str = Query(default="expiry_date"),
    sort_order: int = Query(default=1, ge=-1, le=1),
    batch_service: BatchService = Depends(get_batch_service),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST,
        )
    ),
):
    result = await batch_service.get_all_batches(
        current_user=current_user,
        page=page,
        limit=limit,
        medicine_id=medicine_id,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    # Extract raw data safely
    items = result.get("items", [])
    total = result.get("total", len(items))
    total_pages = result.get("total_pages", (total + limit - 1) // limit if limit else 1)

    # Return with exact pagination schema fields required by Pydantic
    return {
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "total_records": total,            # Added missing field
            "has_next": page < total_pages,   # Added missing field
            "has_previous": page > 1,          # Added missing field
        },
    }

# -------------------- Get Batches By Medicine -------------------- #

@router.get(
    "/medicine/{medicine_id}",
    response_model=list[BatchResponse]
)
async def get_batches_by_medicine(
    medicine_id: str,
    batch_service: BatchService = Depends(
        get_batch_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST
        )
    )
):
    return await batch_service.get_batches_by_medicine(
        current_user=current_user,
        medicine_id=medicine_id
    )


# -------------------- Get Expired Batches -------------------- #

@router.get(
    "/expired",
    response_model=list[BatchResponse]
)
async def get_expired_batches(
    batch_service: BatchService = Depends(
        get_batch_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await batch_service.get_expired_batches(
        current_user=current_user,
        today=date.today()
    )


# -------------------- Get Batch By ID -------------------- #

@router.get(
    "/{batch_id}",
    response_model=BatchResponse
)
async def get_batch_by_id(
    batch_id: str,
    batch_service: BatchService = Depends(
        get_batch_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.DOCTOR,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.RECEPTIONIST
        )
    )
):
    return await batch_service.get_batch_by_id(
        current_user=current_user,
        batch_id=batch_id
    )


# -------------------- Update Batch -------------------- #

@router.patch(
    "/{batch_id}",
    response_model=BatchResponse,
    status_code=status.HTTP_200_OK
)
async def update_batch(
    batch_id: str,
    batch_data: BatchUpdate,
    batch_service: BatchService = Depends(
        get_batch_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await batch_service.update_batch(
        current_user=current_user,
        batch_id=batch_id,
        batch_data=batch_data
    )