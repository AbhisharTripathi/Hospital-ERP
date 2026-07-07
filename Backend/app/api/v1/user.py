from fastapi import APIRouter, Depends, status

from app.dependencies import (
   
    get_user_service,
    require_role
)

from app.models.user import UserRole

from app.schemas.user import (
    EmployeeCreate,
    EmployeeResponse
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