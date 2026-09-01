# from fastapi import (
#     APIRouter,
#     Depends,
#     Query
# )

# from app.dependencies import (
#     get_pharmacy_service,
#     require_role
# )

# from app.models.user import UserRole

# from app.models.pharmacy import PharmacyStatus

# from app.schemas.pharmacy import (
#     PharmacyCreate,
#     PharmacyUpdate,
#     PharmacyStatusUpdate
# )

# router = APIRouter(
#     prefix="/pharmacy",
#     tags=["Pharmacy"]
# )


# # ==========================================
# # Create Pharmacy Order
# # ==========================================

# @router.post("")

# async def create_pharmacy(

#     pharmacy_data: PharmacyCreate,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.create_pharmacy(

#         hospital_id=current_user["hospital_id"],

#         pharmacy_data=pharmacy_data,

#         current_user=current_user

#     )


# # ==========================================
# # Get Pharmacy By ID
# # ==========================================

# @router.get("/{pharmacy_id}")

# async def get_pharmacy_by_id(

#     pharmacy_id: str,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.DOCTOR,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN,
#             UserRole.RECEPTIONIST

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.get_by_pharmacy_id(

#         hospital_id=current_user["hospital_id"],

#         pharmacy_id=pharmacy_id

#     )


# # ==========================================
# # Get Patient Pharmacy History
# # ==========================================

# @router.get("/patient/{patient_id}")

# async def get_patient_pharmacy(

#     patient_id: str,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.DOCTOR,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN,
#             UserRole.RECEPTIONIST

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.get_patient_pharmacy(

#         hospital_id=current_user["hospital_id"],

#         patient_id=patient_id

#     )


# # ==========================================
# # Get All Pharmacy Orders
# # ==========================================

# @router.get("")

# async def get_all_pharmacy(

#     page: int = 1,

#     limit: int = 20,

#     search: str | None = None,

#     patient_id: str | None = None,

#     doctor_id: str | None = None,

#     pharmacist_id: str | None = None,

#     status: PharmacyStatus | None = Query(
#         default=None
#     ),

#     sort_by: str = "created_at",

#     sort_order: int = -1,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.DOCTOR,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN,
#             UserRole.RECEPTIONIST

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.get_all_pharmacy(

#         hospital_id=current_user["hospital_id"],

#         page=page,

#         limit=limit,

#         search=search,

#         patient_id=patient_id,

#         doctor_id=doctor_id,

#         pharmacist_id=pharmacist_id,

#         status=status,

#         sort_by=sort_by,

#         sort_order=sort_order

#     )


# # ==========================================
# # Update Pharmacy
# # ==========================================

# @router.put("/{pharmacy_id}")

# async def update_pharmacy(

#     pharmacy_id: str,

#     pharmacy_data: PharmacyUpdate,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.update_pharmacy(

#         hospital_id=current_user["hospital_id"],

#         pharmacy_id=pharmacy_id,

#         pharmacy_data=pharmacy_data

#     )


# # ==========================================
# # Update Status
# # ==========================================

# @router.patch("/{pharmacy_id}/status")

# async def update_status(

#     pharmacy_id: str,

#     status_data: PharmacyStatusUpdate,

#     current_user=Depends(

#         require_role(

#             UserRole.PHARMACIST,
#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.update_status(

#         hospital_id=current_user["hospital_id"],

#         pharmacy_id=pharmacy_id,

#         status_data=status_data,

#         current_user=current_user

#     )


# # ==========================================
# # Delete Pharmacy
# # ==========================================

# @router.delete("/{pharmacy_id}")

# async def delete_pharmacy(

#     pharmacy_id: str,

#     current_user=Depends(

#         require_role(

#             UserRole.ADMIN,
#             UserRole.SUPER_ADMIN

#         )

#     ),

#     pharmacy_service=Depends(
#         get_pharmacy_service
#     )

# ):

#     return await pharmacy_service.delete_pharmacy(

#         hospital_id=current_user["hospital_id"],

#         pharmacy_id=pharmacy_id

#     )

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from app.dependencies import (
    get_pharmacy_service,
    require_role
)
from app.models.pharmacy import PharmacyStatus
from app.models.user import UserRole
from app.schemas.pagination import PaginatedResponse
from app.schemas.pharmacy import (
    PharmacyCreate,
    PharmacyResponse,
    PharmacyStatusUpdate,
    PharmacyUpdate
)
from app.services.pharmacy import PharmacyService

router = APIRouter(
    prefix="/pharmacy",
    tags=["Pharmacy"]
)


# -------------------- Create Pharmacy Order -------------------- #

@router.post(
    "",
    response_model=PharmacyResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_pharmacy(
    pharmacy_data: PharmacyCreate,
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await pharmacy_service.create_pharmacy(
        hospital_id=current_user["hospital_id"],
        pharmacy_data=pharmacy_data,
        current_user=current_user
    )


# -------------------- Get All Pharmacy Orders -------------------- #

@router.get(
    "",
    response_model=PaginatedResponse[PharmacyResponse]
)
async def get_all_pharmacy(
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
        default=None
    ),
    patient_id: str | None = Query(
        default=None
    ),
    doctor_id: str | None = Query(
        default=None
    ),
    pharmacist_id: str | None = Query(
        default=None
    ),
    status: PharmacyStatus | None = Query(
        default=None
    ),
    sort_by: str = Query(
        default="created_at"
    ),
    sort_order: int = Query(
        default=-1
    ),
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
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
    return await pharmacy_service.get_all_pharmacy(
        hospital_id=current_user["hospital_id"],
        page=page,
        limit=limit,
        search=search,
        patient_id=patient_id,
        doctor_id=doctor_id,
        pharmacist_id=pharmacist_id,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order
    )


# -------------------- Get Patient Pharmacy History -------------------- #

@router.get(
    "/patient/{patient_id}",
    response_model=list[PharmacyResponse]
)
async def get_patient_pharmacy(
    patient_id: str,
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
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
    return await pharmacy_service.get_patient_pharmacy(
        hospital_id=current_user["hospital_id"],
        patient_id=patient_id
    )


# -------------------- Get Pharmacy By ID -------------------- #

@router.get(
    "/{pharmacy_id}",
    response_model=PharmacyResponse
)
async def get_pharmacy_by_id(
    pharmacy_id: str,
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
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
    return await pharmacy_service.get_by_pharmacy_id(
        hospital_id=current_user["hospital_id"],
        pharmacy_id=pharmacy_id
    )


# -------------------- Update Pharmacy -------------------- #

@router.patch(
    "/{pharmacy_id}",
    response_model=PharmacyResponse,
    status_code=status.HTTP_200_OK
)
async def update_pharmacy(
    pharmacy_id: str,
    pharmacy_data: PharmacyUpdate,
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await pharmacy_service.update_pharmacy(
        hospital_id=current_user["hospital_id"],
        pharmacy_id=pharmacy_id,
        pharmacy_data=pharmacy_data
    )


# -------------------- Update Status -------------------- #

@router.patch(
    "/{pharmacy_id}/status",
    response_model=PharmacyResponse,
    status_code=status.HTTP_200_OK
)
async def update_status(
    pharmacy_id: str,
    status_data: PharmacyStatusUpdate,
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
    ),
    current_user=Depends(
        require_role(
            UserRole.PHARMACIST,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await pharmacy_service.update_status(
        hospital_id=current_user["hospital_id"],
        pharmacy_id=pharmacy_id,
        status_data=status_data,
        current_user=current_user
    )


# -------------------- Delete Pharmacy -------------------- #

@router.delete(
    "/{pharmacy_id}",
    status_code=status.HTTP_200_OK
)
async def delete_pharmacy(
    pharmacy_id: str,
    pharmacy_service: PharmacyService = Depends(
        get_pharmacy_service
    ),
    current_user=Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    )
):
    return await pharmacy_service.delete_pharmacy(
        hospital_id=current_user["hospital_id"],
        pharmacy_id=pharmacy_id
    )