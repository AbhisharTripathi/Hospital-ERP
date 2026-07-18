from fastapi import APIRouter, Depends, status

from app.dependencies import (
    get_department_service,
    require_role
)

from app.models.user import UserRole

from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    UpdateDepartmentStatus
)

from app.services.department import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_department(
    department_data: DepartmentCreate,
    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),
    department_service: DepartmentService = Depends(
        get_department_service
    )
):

    return await department_service.create_department(
        current_user=current_user,
        department_data=department_data
    )

@router.get(
    "",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_departments(

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    department_service: DepartmentService = Depends(
        get_department_service
    )

):

    return await department_service.get_all_departments(
        current_user=current_user
    )


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK
)
async def get_department_by_id(

    department_id: str,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    department_service: DepartmentService = Depends(
        get_department_service
    )
):

    return await department_service.get_department_by_id(
        current_user=current_user,
        department_id=department_id
    )

@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK
)
async def update_department(

    department_id: str,

    department_data: DepartmentUpdate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    department_service: DepartmentService = Depends(
        get_department_service
    )
):

    return await department_service.update_department(
        current_user=current_user,
        department_id=department_id,
        department_data=department_data
    )

@router.patch(
    "/{department_id}/status",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK
)
async def update_department_status(

    department_id: str,

    status_data: UpdateDepartmentStatus,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    department_service: DepartmentService = Depends(
        get_department_service
    )
):

    return await department_service.update_department_status(
        current_user=current_user,
        department_id=department_id,
        status_data=status_data
    )































