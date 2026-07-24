from fastapi import (
    HTTPException,
    status
)

from app.models.lab_order import (
    LabOrderModel,
    LabOrderStatus
)

from app.schemas.lab_order import (
    LabOrderCreate
)

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)

from app.utils.id_generator import (
    IDGenerator
)


class LabOrderService:

    def __init__(

        self,

        lab_order_repository,

        appointment_repository,

        patient_repository,

        doctor_repository,

        counter_repository

    ):

        self.lab_order_repo = lab_order_repository

        self.appointment_repo = appointment_repository

        self.patient_repo = patient_repository

        self.doctor_repo = doctor_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Create Lab Order
    # ==========================================

    async def create_lab_order(

        self,

        hospital_id: str,

        current_user,

        lab_order_data: LabOrderCreate

    ):

        # -------------------------------
        # Appointment Exists
        # -------------------------------

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id,

            lab_order_data.appointment_id

        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        # -------------------------------
        # Patient Exists
        # -------------------------------

        patient = await self.patient_repo.get_patient_by_id(

            hospital_id,

            appointment["patient_id"]

        )

        if not patient:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Patient not found"

            )

        # -------------------------------
        # Doctor Exists
        # -------------------------------

        doctor = await self.doctor_repo.get_doctor_by_id(

            appointment["doctor_id"],

            hospital_id

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )

        # -------------------------------
        # One Lab Order Per Appointment
        # -------------------------------

        existing = await self.lab_order_repo.get_by_appointment_id(

            hospital_id,

            lab_order_data.appointment_id

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Lab order already exists for this appointment"

            )

        # -------------------------------
        # Generate Lab Order ID
        # -------------------------------

        lab_order_id = await IDGenerator.generate_lab_order_id(

            self.counter_repo

        )

        lab_order = LabOrderModel(

            lab_order_id=lab_order_id,

            hospital_id=hospital_id,

            patient_id=appointment["patient_id"],

            doctor_id=appointment["doctor_id"],

            appointment_id=appointment["appointment_id"],

            tests=lab_order_data.tests,

            priority=lab_order_data.priority,

            clinical_notes=lab_order_data.clinical_notes,

            expected_date=lab_order_data.expected_date,

            status=LabOrderStatus.ORDERED,

            ordered_by=current_user["user_id"]

        )

        await self.lab_order_repo.create_lab_order(

            lab_order.model_dump()

        )

        return {

            "success": True,

            "message": "Lab order created successfully",

            "lab_order_id": lab_order_id

        }

    # ==========================================
    # Get Lab Order By ID
    # ==========================================

    async def get_by_lab_order_id(

        self,

        hospital_id: str,

        lab_order_id: str

    ):

        lab_order = await self.lab_order_repo.get_by_lab_order_id(

            hospital_id,

            lab_order_id

        )

        if not lab_order:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Lab order not found"

            )

        return lab_order

    # ==========================================
    # Get Patient Lab Orders
    # ==========================================

    async def get_patient_lab_orders(

        self,

        hospital_id: str,

        patient_id: str

    ):

        patient = await self.patient_repo.get_patient_by_id(

            hospital_id,

            patient_id

        )

        if not patient:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Patient not found"

            )

        return await self.lab_order_repo.get_by_patient(

            hospital_id,

            patient_id

        )
        # ==========================================
    # Get All Lab Orders
    # ==========================================

    async def get_all_lab_orders(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: LabOrderStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        result = await self.lab_order_repo.get_all_lab_orders(

            hospital_id=hospital_id,

            page=page,

            limit=limit,

            search=search,

            doctor_id=doctor_id,

            patient_id=patient_id,

            status=status,

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
    # Update Lab Order
    # ==========================================

    async def update_lab_order(

        self,

        hospital_id: str,

        lab_order_id: str,

        lab_order_data

    ):

        lab_order = await self.lab_order_repo.get_by_lab_order_id(

            hospital_id,

            lab_order_id

        )

        if not lab_order:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Lab order not found"

            )

        update_data = lab_order_data.model_dump(

            exclude_unset=True,

            exclude_none=True

        )

        await self.lab_order_repo.update_lab_order(

            hospital_id,

            lab_order_id,

            update_data

        )

        return {

            "success": True,

            "message": "Lab order updated successfully"

        }

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        lab_order_id: str,

        status_data

    ):

        lab_order = await self.lab_order_repo.get_by_lab_order_id(

            hospital_id,

            lab_order_id

        )

        if not lab_order:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Lab order not found"

            )

        await self.lab_order_repo.update_status(

            hospital_id,

            lab_order_id,

            status_data.status

        )

        return {

            "success": True,

            "message": "Lab order status updated successfully"

        }

    # ==========================================
    # Upload Report
    # ==========================================

    async def upload_report(

        self,

        hospital_id: str,

        lab_order_id: str,

        report_data

    ):

        lab_order = await self.lab_order_repo.get_by_lab_order_id(

            hospital_id,

            lab_order_id

        )

        if not lab_order:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Lab order not found"

            )

        await self.lab_order_repo.upload_report(

            hospital_id,

            lab_order_id,

            report_data.report_file

        )

        return {

            "success": True,

            "message": "Lab report uploaded successfully"

        }

    # ==========================================
    # Delete Lab Order
    # ==========================================

    async def delete_lab_order(

        self,

        hospital_id: str,

        lab_order_id: str

    ):

        lab_order = await self.lab_order_repo.get_by_lab_order_id(

            hospital_id,

            lab_order_id

        )

        if not lab_order:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Lab order not found"

            )

        await self.lab_order_repo.delete_lab_order(

            hospital_id,

            lab_order_id

        )

        return {

            "success": True,

            "message": "Lab order deleted successfully"

        }