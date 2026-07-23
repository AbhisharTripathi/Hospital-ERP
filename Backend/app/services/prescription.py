from fastapi import (
    HTTPException,
    status
)

from app.models.prescription import (
    PrescriptionModel,
    PrescriptionStatus
)

from app.schemas.prescription import (
    PrescriptionCreate
)

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)

from app.utils.id_generator import (
    IDGenerator
)


class PrescriptionService:

    def __init__(

        self,

        prescription_repository,

        appointment_repository,

        patient_repository,

        doctor_repository,

        counter_repository

    ):

        self.prescription_repo = prescription_repository

        self.appointment_repo = appointment_repository

        self.patient_repo = patient_repository

        self.doctor_repo = doctor_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Create Prescription
    # ==========================================

    async def create_prescription(

        self,

        hospital_id: str,

        current_user,

        prescription_data: PrescriptionCreate

    ):

        # -------------------------------
        # Appointment Exists
        # -------------------------------

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id,

            prescription_data.appointment_id

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

            prescription_data.patient_id

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

            prescription_data.doctor_id,

            hospital_id

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )

        # -------------------------------
        # One Prescription Per Appointment
        # -------------------------------

        existing = await self.prescription_repo.get_by_appointment_id(

            hospital_id,

            prescription_data.appointment_id

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Prescription already exists for this appointment"

            )

        # -------------------------------
        # Generate Prescription ID
        # -------------------------------

        prescription_id = await IDGenerator.generate_prescription_id(

            self.counter_repo

        )

        prescription = PrescriptionModel(

            prescription_id=prescription_id,

            hospital_id=hospital_id,

            appointment_id=prescription_data.appointment_id,

            patient_id=prescription_data.patient_id,

            doctor_id=prescription_data.doctor_id,

            diagnosis=prescription_data.diagnosis,

            advice=prescription_data.advice,

            follow_up_date=prescription_data.follow_up_date,

            medicines=prescription_data.medicines,

            status=PrescriptionStatus.ACTIVE,

            created_by=current_user["user_id"]

        )

        await self.prescription_repo.create_prescription(

            prescription.model_dump()

        )

        return {

            "success": True,

            "message": "Prescription created successfully",

            "prescription_id": prescription_id

        }
        # ==========================================
    # Get Prescription By ID
    # ==========================================

    async def get_by_prescription_id(

        self,

        hospital_id: str,

        prescription_id: str

    ):

        prescription = await self.prescription_repo.get_by_prescription_id(

            hospital_id,

            prescription_id

        )

        if not prescription:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Prescription not found"

            )

        return prescription

    # ==========================================
    # Get Patient Prescriptions
    # ==========================================

    async def get_patient_prescriptions(

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

        return await self.prescription_repo.get_by_patient(

            hospital_id,

            patient_id

        )

    # ==========================================
    # Get All Prescriptions
    # ==========================================

    async def get_all_prescriptions(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: PrescriptionStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        result = await self.prescription_repo.get_all_prescriptions(

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
    # Update Prescription
    # ==========================================

    async def update_prescription(

        self,

        hospital_id: str,

        prescription_id: str,

        prescription_data

    ):

        prescription = await self.prescription_repo.get_by_prescription_id(

            hospital_id,

            prescription_id

        )

        if not prescription:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Prescription not found"

            )

        update_data = prescription_data.model_dump(

            exclude_unset=True,

            exclude_none=True

        )

        await self.prescription_repo.update_prescription(

            hospital_id,

            prescription_id,

            update_data

        )

        return {

            "success": True,

            "message": "Prescription updated successfully"

        }

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        prescription_id: str,

        status_data

    ):

        prescription = await self.prescription_repo.get_by_prescription_id(

            hospital_id,

            prescription_id

        )

        if not prescription:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Prescription not found"

            )

        await self.prescription_repo.update_status(

            hospital_id,

            prescription_id,

            status_data.status

        )

        return {

            "success": True,

            "message": "Prescription status updated successfully"

        }

    # ==========================================
    # Delete Prescription
    # ==========================================

    async def delete_prescription(

        self,

        hospital_id: str,

        prescription_id: str

    ):

        prescription = await self.prescription_repo.get_by_prescription_id(

            hospital_id,

            prescription_id

        )

        if not prescription:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Prescription not found"

            )

        await self.prescription_repo.delete_prescription(

            hospital_id,

            prescription_id

        )

        return {

            "success": True,

            "message": "Prescription deleted successfully"

        }