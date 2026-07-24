from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies import (
    get_user_service,
    require_role,
    
)
from fastapi import Query
from app.models.user import UserRole,UserStatus
from app.schemas.user import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,UpdateEmployeeStatus
)
from app.schemas.pagination import PaginatedResponse
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),
    user_service: UserService = Depends(
        get_user_service
    )
):
    return await user_service.create_employee(
        current_user=current_user,
        employee_data=employee_data
    )

@router.get(
    "",
    response_model=PaginatedResponse[EmployeeResponse]
)
async def get_all_users(

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

    role: UserRole | None = Query(
        default=None
    ),

    status: UserStatus | None = Query(
        default=None
    ),

    sort_by: str = Query(
        default="created_at"
    ),

    sort_order: int = Query(
        default=-1
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    user_service: UserService = Depends(
        get_user_service
    )

):

    return await user_service.get_all_employees(

        current_user=current_user,

        page=page,

        limit=limit,

        search=search,

        role=role,

        status=status,

        sort_by=sort_by,

        sort_order=sort_order

    )

@router.get(
    "/{user_id}",
    response_model=EmployeeResponse
)
async def get_employee(
    user_id: str,
    
    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),
    user_service: UserService = Depends(
        get_user_service
    )
):
    
    return await user_service.get_employee(
        current_user,
        user_id
    )

@router.patch(
    "/{user_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK
)
async def update_employee(
    user_id: str,
    employee_data: EmployeeUpdate,
    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),
    user_service: UserService = Depends(
        get_user_service
    )
):
    return await user_service.update_employee(
        current_user=current_user,
        user_id=user_id,
        employee_data=employee_data
    )


@router.patch(
    "/{user_id}/status",
    status_code=status.HTTP_200_OK
)
async def update_employee_status(
    user_id: str,
    status_data: UpdateEmployeeStatus,
    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),
    user_service: UserService = Depends(
        get_user_service
    )
):

    return await user_service.update_employee_status(
        current_user=current_user,
        user_id=user_id,
        status_data=status_data
    )