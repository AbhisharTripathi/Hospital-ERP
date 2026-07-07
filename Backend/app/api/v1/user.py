from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies import (
    get_user_service,
    require_role,
    
)
from app.models.user import UserRole
from app.schemas.user import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)
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
    response_model=list[EmployeeResponse]
)
async def get_all_users(
   
    current_user: dict = Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),
    user_service: UserService = Depends(
        get_user_service
    )
):
    
    return await user_service.get_all_employees(current_user)

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