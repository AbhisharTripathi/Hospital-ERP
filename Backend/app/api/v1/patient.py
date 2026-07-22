from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from app.dependencies import (
    get_patient_services,
    require_role
)

from app.models.patient import PatientStatus

from app.models.user import UserRole

from app.schemas.pagination import PaginatedResponse

from app.schemas.patient import (
    PatientCreate,
    PatientResponse,
    PatientUpdate
)

from app.services.patient import PatientServices


router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)


@router.post(
    "",
    response_model=PatientResponse
)
async def create_patient(

    patient: PatientCreate,

    patient_services: PatientServices = Depends(
        get_patient_services
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST
        )
    )

):
    try:

        result = await patient_services.create_patient(
            patient=patient,
            
            current_user=current_user
        )

        patient_data = await patient_services.get_patient_by_id(
            patient_id=result["patient_id"],
            current_user=current_user
        )

        return patient_data

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error : {str(e)}"
        )


@router.get(
    "",
    response_model=PaginatedResponse[PatientResponse]
)
async def get_all_patients(

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

    patient_status: PatientStatus | None = Query(
        default=None
    ),

    sort_by: str = Query(
        default="created_at"
    ),

    sort_order: int = Query(
        default=-1
    ),

    patient_services: PatientServices = Depends(
        get_patient_services
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE
        )
    )

):

    return await patient_services.get_all_patients(

        current_user=current_user,

        page=page,

        limit=limit,

        search=search,

        status=patient_status,

        sort_by=sort_by,

        sort_order=sort_order

    )


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
async def get_patient_by_id(

    patient_id: str,

    patient_services: PatientServices = Depends(
        get_patient_services
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE
        )
    )

):

    return await patient_services.get_patient_by_id(
        patient_id=patient_id,
        current_user=current_user
    )


@router.put(
    "/{patient_id}"
)
async def update_patient(

    patient_id: str,

    patient_update: PatientUpdate,

    patient_services: PatientServices = Depends(
        get_patient_services
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST
        )
    )

):

    return await patient_services.update_patient(

        patient_id=patient_id,

        patient_update=patient_update,

        current_user=current_user

    )


@router.patch(
    "/{patient_id}/deactivate"
)
async def deactivate_patient(

    patient_id: str,

    patient_services: PatientServices = Depends(
        get_patient_services
    ),

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    )

):

    return await patient_services.deactivate_patient(

        patient_id=patient_id,

        current_user=current_user

    )