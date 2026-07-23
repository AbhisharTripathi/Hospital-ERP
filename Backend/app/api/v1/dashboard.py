from fastapi import (
    APIRouter,
    Depends
)

from app.dependencies import (
    get_dashboard_service,
    require_role
)

from app.models.user import UserRole

from app.schemas.dashboard import (
    DashboardResponse
)

from app.services.dashboard import (
    DashboardService
)


router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]

)


@router.get(

    "/admin",

    response_model=DashboardResponse

)
async def get_admin_dashboard(

    current_user=Depends(

        require_role(

            UserRole.SUPER_ADMIN,

            UserRole.ADMIN

        )

    ),

    dashboard_service: DashboardService = Depends(

        get_dashboard_service

    )

):

    return await dashboard_service.get_admin_dashboard(

        current_user

    )