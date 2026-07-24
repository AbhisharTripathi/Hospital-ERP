from fastapi import (
    APIRouter,
    Depends,
    Query
)

from app.dependencies import (
    get_billing_service,
    require_role
)

from app.models.billing import PaymentStatus
from app.models.user import UserRole

from app.schemas.billing import (
    BillingCreate,
    BillingUpdate,
    BillingStatusUpdate
)

router = APIRouter(
    prefix="/billings",
    tags=["Billing"]
)


# ==========================================
# Create Bill
# ==========================================

@router.post("")

async def create_bill(

    billing_data: BillingCreate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.ACCOUNTANT
        )
    ),

    billing_service=Depends(
        get_billing_service
    )

):

    return await billing_service.create_bill(

        hospital_id=current_user["hospital_id"],

        billing_data=billing_data,

        current_user=current_user

    )


# ==========================================
# Get Bill By ID
# ==========================================

@router.get("/{bill_id}")

async def get_bill(

    bill_id: str,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.RECEPTIONIST
        )
    ),

    billing_service=Depends(
        get_billing_service
    )

):

    return await billing_service.get_bill_by_id(

        hospital_id=current_user["hospital_id"],

        bill_id=bill_id

    )


# ==========================================
# Get All Bills
# ==========================================

@router.get("")

async def get_all_bills(

    page: int = Query(1, ge=1),

    limit: int = Query(10, ge=1, le=100),

    search: str | None = None,

    patient_id: str | None = None,

    doctor_id: str | None = None,

    payment_status: PaymentStatus | None = None,

    sort_by: str = "created_at",

    sort_order: int = -1,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.RECEPTIONIST
        )
    ),

    billing_service=Depends(
        get_billing_service
    )

):

    return await billing_service.get_all_bills(

        hospital_id=current_user["hospital_id"],

        page=page,

        limit=limit,

        search=search,

        patient_id=patient_id,

        doctor_id=doctor_id,

        payment_status=payment_status,

        sort_by=sort_by,

        sort_order=sort_order

    )


# ==========================================
# Update Bill
# ==========================================

@router.put("/{bill_id}")

async def update_bill(

    bill_id: str,

    billing_data: BillingUpdate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.ACCOUNTANT
        )
    ),

    billing_service=Depends(
        get_billing_service
    )

):

    return await billing_service.update_bill(

        hospital_id=current_user["hospital_id"],

        bill_id=bill_id,

        billing_data=billing_data

    )


# ==========================================
# Update Payment Status
# ==========================================

@router.patch("/{bill_id}/payment-status")

async def update_payment_status(

    bill_id: str,

    payment_data: BillingStatusUpdate,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.ACCOUNTANT
        )
    ),

    billing_service=Depends(
        get_billing_service
    )

):

    return await billing_service.update_payment_status(

        hospital_id=current_user["hospital_id"],

        bill_id=bill_id,

        payment_status=payment_data.payment_status

    )


# ==========================================
# Delete Bill
# ==========================================

@router.delete("/{bill_id}")

async def delete_bill(

    bill_id: str,

    current_user=Depends(
        require_role(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN
        )
    ),

    billing_service=Depends(
        get_billing_service
    )

):

    return await billing_service.delete_bill(

        hospital_id=current_user["hospital_id"],

        bill_id=bill_id

    )