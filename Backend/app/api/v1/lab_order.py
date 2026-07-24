from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_lab_order_service,
    require_role
)

from app.models.user import UserRole

from app.models.lab_order import (
    LabOrderStatus
)

from app.schemas.lab_order import (
    LabOrderCreate,
    LabOrderUpdate,
    LabOrderStatusUpdate,
    LabReportUpload
)

router = APIRouter(
    prefix="/lab-orders",
    tags=["Lab Orders"]
)


# ==========================================
# Create Lab Order
# ==========================================

@router.post("")

async def create_lab_order(

    lab_order_data: LabOrderCreate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.create_lab_order(

        hospital_id=current_user["hospital_id"],

        current_user=current_user,

        lab_order_data=lab_order_data

    )


# ==========================================
# Get Lab Order By ID
# ==========================================

@router.get("/{lab_order_id}")

async def get_lab_order_by_id(

    lab_order_id: str,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN,

            UserRole.RECEPTIONIST,

            UserRole.LAB_TECHNICIAN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.get_by_lab_order_id(

        hospital_id=current_user["hospital_id"],

        lab_order_id=lab_order_id

    )


# ==========================================
# Patient History
# ==========================================

@router.get("/patient/{patient_id}")

async def get_patient_lab_orders(

    patient_id: str,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN,

            UserRole.RECEPTIONIST,

            UserRole.LAB_TECHNICIAN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.get_patient_lab_orders(

        hospital_id=current_user["hospital_id"],

        patient_id=patient_id

    )


# ==========================================
# Get All
# ==========================================

@router.get("")

async def get_all_lab_orders(

    page: int = 1,

    limit: int = 20,

    search: str | None = None,

    doctor_id: str | None = None,

    patient_id: str | None = None,

    status: LabOrderStatus | None = Query(
        default=None
    ),

    sort_by: str = "created_at",

    sort_order: int = -1,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN,

            UserRole.RECEPTIONIST,

            UserRole.LAB_TECHNICIAN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.get_all_lab_orders(

        hospital_id=current_user["hospital_id"],

        page=page,

        limit=limit,

        search=search,

        doctor_id=doctor_id,

        patient_id=patient_id,

        status=status,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Update
# ==========================================

@router.put("/{lab_order_id}")

async def update_lab_order(

    lab_order_id: str,

    lab_order_data: LabOrderUpdate,

    current_user=Depends(

        require_role(

            UserRole.DOCTOR,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.update_lab_order(

        hospital_id=current_user["hospital_id"],

        lab_order_id=lab_order_id,

        lab_order_data=lab_order_data

    )


# ==========================================
# Update Status
# ==========================================

@router.patch("/{lab_order_id}/status")

async def update_lab_order_status(

    lab_order_id: str,

    status_data: LabOrderStatusUpdate,

    current_user=Depends(

        require_role(

            UserRole.LAB_TECHNICIAN,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.update_status(

        hospital_id=current_user["hospital_id"],

        lab_order_id=lab_order_id,

        status_data=status_data

    )


# ==========================================
# Upload Report
# ==========================================

@router.patch("/{lab_order_id}/upload-report")

async def upload_report(

    lab_order_id: str,

    report_data: LabReportUpload,

    current_user=Depends(

        require_role(

            UserRole.LAB_TECHNICIAN,

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.upload_report(

        hospital_id=current_user["hospital_id"],

        lab_order_id=lab_order_id,

        report_data=report_data

    )


# ==========================================
# Delete
# ==========================================

@router.delete("/{lab_order_id}")

async def delete_lab_order(

    lab_order_id: str,

    current_user=Depends(

        require_role(

            UserRole.ADMIN,

            UserRole.SUPER_ADMIN

        )

    ),

    lab_order_service=Depends(
        get_lab_order_service
    )

):

    return await lab_order_service.delete_lab_order(

        hospital_id=current_user["hospital_id"],

        lab_order_id=lab_order_id

    )