from fastapi import (
    HTTPException,
    status
)

from app.models.consultation import (
    ConsultationModel,
    ConsultationStatus
)

from app.schemas.consultation import (
    ConsultationCreate
)

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)

from app.utils.id_generator import (
    IDGenerator
)


class ConsultationService:

    def __init__(

        self,

        consultation_repository,

        appointment_repository,

        patient_repository,

        doctor_repository,

        counter_repository

    ):

        self.consultation_repo = consultation_repository

        self.appointment_repo = appointment_repository

        self.patient_repo = patient_repository

        self.doctor_repo = doctor_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Create Consultation
    # ==========================================

    async def create_consultation(

        self,

        hospital_id: str,

        current_user,

        consultation_data: ConsultationCreate

    ):

        # -------------------------------
        # Appointment Exists
        # -------------------------------

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id,

            consultation_data.appointment_id

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
        # Only One Consultation Per Appointment
        # -------------------------------

        existing = await self.consultation_repo.get_by_appointment_id(

            hospital_id,

            consultation_data.appointment_id

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Consultation already exists for this appointment"

            )

        # -------------------------------
        # Generate Consultation ID
        # -------------------------------

        consultation_id = await IDGenerator.generate_consultation_id(

            self.counter_repo

        )

        consultation = ConsultationModel(

            consultation_id=consultation_id,

            hospital_id=hospital_id,

            appointment_id=appointment["appointment_id"],

            patient_id=appointment["patient_id"],

            doctor_id=appointment["doctor_id"],

            chief_complaint=consultation_data.chief_complaint,

            history_of_present_illness=consultation_data.history_of_present_illness,

            physical_examination=consultation_data.physical_examination,

            diagnosis=consultation_data.diagnosis,

            clinical_notes=consultation_data.clinical_notes,

            advice=consultation_data.advice,

            follow_up_date=consultation_data.follow_up_date,

            status=ConsultationStatus.IN_PROGRESS,

            created_by=current_user["user_id"]

        )

        await self.consultation_repo.create_consultation(

            consultation.model_dump()

        )

        return {

            "success": True,

            "message": "Consultation created successfully",

            "consultation_id": consultation_id

        }

    # ==========================================
    # Get Consultation By ID
    # ==========================================

    async def get_by_consultation_id(

        self,

        hospital_id: str,

        consultation_id: str

    ):

        consultation = await self.consultation_repo.get_by_consultation_id(

            hospital_id,

            consultation_id

        )

        if not consultation:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Consultation not found"

            )

        return consultation

    # ==========================================
    # Get Patient Consultation History
    # ==========================================

    async def get_patient_consultations(

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

        return await self.consultation_repo.get_by_patient(

            hospital_id,

            patient_id

        )
        # ==========================================
    # Get All Consultations
    # ==========================================

    async def get_all_consultations(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: ConsultationStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        result = await self.consultation_repo.get_all_consultations(

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
    # Update Consultation
    # ==========================================

    async def update_consultation(

        self,

        hospital_id: str,

        consultation_id: str,

        consultation_data

    ):

        consultation = await self.consultation_repo.get_by_consultation_id(

            hospital_id,

            consultation_id

        )

        if not consultation:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Consultation not found"

            )

        update_data = consultation_data.model_dump(

            exclude_unset=True,

            exclude_none=True

        )

        await self.consultation_repo.update_consultation(

            hospital_id,

            consultation_id,

            update_data

        )

        return {

            "success": True,

            "message": "Consultation updated successfully"

        }

    # ==========================================
    # Update Consultation Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        consultation_id: str,

        status_data

    ):

        consultation = await self.consultation_repo.get_by_consultation_id(

            hospital_id,

            consultation_id

        )

        if not consultation:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Consultation not found"

            )

        await self.consultation_repo.update_status(

            hospital_id,

            consultation_id,

            status_data.status

        )

        return {

            "success": True,

            "message": "Consultation status updated successfully"

        }

    # ==========================================
    # Delete Consultation
    # ==========================================

    async def delete_consultation(

        self,

        hospital_id: str,

        consultation_id: str

    ):

        consultation = await self.consultation_repo.get_by_consultation_id(

            hospital_id,

            consultation_id

        )

        if not consultation:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Consultation not found"

            )

        await self.consultation_repo.delete_consultation(

            hospital_id,

            consultation_id

        )

        return {

            "success": True,

            "message": "Consultation deleted successfully"

        }