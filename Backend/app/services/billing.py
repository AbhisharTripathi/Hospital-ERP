from fastapi import (
    HTTPException,
    status
)

from app.models.billing import (
    BillingModel,
    PaymentStatus
)

from app.schemas.billing import (
    BillingCreate,
    BillingUpdate
)

from app.utils.id_generator import IDGenerator
from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)


class BillingService:

    def __init__(

        self,

        billing_repository,

        patient_repository,

        doctor_repository,

        appointment_repository,

        counter_repository

    ):

        self.billing_repo = billing_repository

        self.patient_repo = patient_repository

        self.doctor_repo = doctor_repository

        self.appointment_repo = appointment_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Helper
    # ==========================================

    def calculate_total(

        self,

        items,

        discount: float,

        tax: float

    ):

        subtotal = 0

        bill_items = []

        for item in items:

            total_price = (
                item.quantity *
                item.unit_price
            )

            subtotal += total_price

            bill_items.append(

                {

                    "item_name": item.item_name,

                    "item_type": item.item_type,

                    "quantity": item.quantity,

                    "unit_price": item.unit_price,

                    "total_price": total_price

                }

            )

        grand_total = (

            subtotal

            -

            discount

            +

            tax

        )

        return (

            bill_items,

            subtotal,

            grand_total

        )

    # ==========================================
    # Create Bill
    # ==========================================

    async def create_bill(

        self,

        hospital_id: str,

        billing_data: BillingCreate,

        current_user

    ):

        appointment = await self.appointment_repo.get_by_appointment_id(
            hospital_id,
            billing_data.appointment_id
        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        patient = await self.patient_repo.get_patient_by_id(

            hospital_id,

            appointment["patient_id"]

        )

        if not patient:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Patient not found"

            )

        doctor = await self.doctor_repo.get_doctor_by_id(

            appointment["doctor_id"],

            hospital_id

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )

        bill_id = await IDGenerator.generate_bill_id(

            self.counter_repo

        )

        invoice_number = bill_id.replace(

            "BILL",

            "INV"

        )

        (

            bill_items,

            subtotal,

            grand_total

        ) = self.calculate_total(

            billing_data.items,

            billing_data.discount,

            billing_data.tax

        )

        bill = BillingModel(

            bill_id=bill_id,

            invoice_number=invoice_number,

            hospital_id=hospital_id,

            patient_id=appointment["patient_id"],

            doctor_id=appointment["doctor_id"],

            appointment_id=appointment["appointment_id"],

            items=bill_items,

            subtotal=subtotal,

            discount=billing_data.discount,

            tax=billing_data.tax,

            grand_total=grand_total,

            payment_status=PaymentStatus.PENDING,

            payment_method=billing_data.payment_method,

            remarks=billing_data.remarks,

            created_by=current_user["user_id"]

        )

        await self.billing_repo.create_bill(

            bill.model_dump()

        )

        return bill

        # ==========================================
    # Get Bill By ID
    # ==========================================

    async def get_bill_by_id(

        self,

        hospital_id: str,

        bill_id: str

    ):

        bill = await self.billing_repo.get_bill_by_id(

            hospital_id,

            bill_id

        )

        if not bill:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Bill not found"

            )

        return bill

    # ==========================================
    # Get All Bills
    # ==========================================

    async def get_all_bills(

        self,

        hospital_id: str,

        page: int,

        limit: int,

        search: str | None,

        patient_id: str | None,

        doctor_id: str | None,

        payment_status: PaymentStatus | None,

        sort_by: str,

        sort_order: int

    ):

        result = await self.billing_repo.get_all_bills(

            hospital_id=hospital_id,

            page=page,

            limit=limit,

            search=search,

            patient_id=patient_id,

            doctor_id=doctor_id,

            payment_status=payment_status,

            sort_by=sort_by,

            sort_order=sort_order

        )

        pagination = build_pagination_meta(

            page=page,

            limit=limit,

            total_records=result["total"]

        )

        return PaginatedResponse(

            data=result["items"],

            pagination=pagination

        )

    # ==========================================
    # Update Bill
    # ==========================================

    async def update_bill(

        self,

        hospital_id: str,

        bill_id: str,

        billing_data: BillingUpdate

    ):

        bill = await self.billing_repo.get_bill_by_id(

            hospital_id,

            bill_id

        )

        if not bill:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Bill not found"

            )

        update_data = billing_data.model_dump(

            exclude_unset=True,

            exclude_none=True

        )

        if "items" in update_data:

            (

                bill_items,

                subtotal,

                grand_total

            ) = self.calculate_total(

                billing_data.items,

                update_data.get(

                    "discount",

                    bill["discount"]

                ),

                update_data.get(

                    "tax",

                    bill["tax"]

                )

            )

            update_data["items"] = bill_items

            update_data["subtotal"] = subtotal

            update_data["grand_total"] = grand_total

        else:

            discount = update_data.get(

                "discount",

                bill["discount"]

            )

            tax = update_data.get(

                "tax",

                bill["tax"]

            )

            grand_total = (

                bill["subtotal"]

                -

                discount

                +

                tax

            )

            update_data["grand_total"] = grand_total

        await self.billing_repo.update_bill(

            hospital_id,

            bill_id,

            update_data

        )

        return {

            "message": "Bill updated successfully"

        }

    # ==========================================
    # Update Payment Status
    # ==========================================

    async def update_payment_status(

        self,

        hospital_id: str,

        bill_id: str,

        payment_status: PaymentStatus

    ):

        bill = await self.billing_repo.get_bill_by_id(

            hospital_id,

            bill_id

        )

        if not bill:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Bill not found"

            )

        await self.billing_repo.update_payment_status(

            hospital_id,

            bill_id,

            payment_status

        )

        return {

            "message": "Payment status updated successfully"

        }

    # ==========================================
    # Delete Bill
    # ==========================================

    async def delete_bill(

        self,

        hospital_id: str,

        bill_id: str

    ):

        bill = await self.billing_repo.get_bill_by_id(

            hospital_id,

            bill_id

        )

        if not bill:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Bill not found"

            )

        await self.billing_repo.delete_bill(

            hospital_id,

            bill_id

        )

        return {

            "message": "Bill deleted successfully"

        }