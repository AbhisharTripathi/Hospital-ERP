from fastapi import (
    HTTPException,
    status
)

from app.models.vitals import (
    VitalModel
)

from app.schemas.vitals import (
    VitalCreate
)

from app.utils.id_generator import (
    IDGenerator
)
from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)



class VitalService:

    def __init__(

        self,

        vital_repository,

        appointment_repository,

        patient_repository,

        doctor_repository,

        counter_repository

    ):

        self.vital_repo = vital_repository

        self.appointment_repo = appointment_repository

        self.patient_repo = patient_repository

        self.doctor_repo = doctor_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Helper
    # ==========================================

    def calculate_bmi(

        self,

        height_cm: float | None,

        weight_kg: float | None

    ):

        if (

            height_cm is None

            or

            weight_kg is None

        ):

            return None

        height_meter = height_cm / 100

        bmi = weight_kg / (height_meter ** 2)

        return round(
            bmi,
            2
        )

    # ==========================================
    # Create Vital
    # ==========================================

    async def create_vital(

        self,

        hospital_id: str,

        current_user,

        vital_data: VitalCreate

    ):

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id,

            vital_data.appointment_id

        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        existing = await self.vital_repo.get_by_appointment(

            hospital_id,

            vital_data.appointment_id

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Vitals already recorded"

            )

        patient = await self.patient_repo.get_patient_by_id(

            hospital_id,

            vital_data.patient_id

        )

        if not patient:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Patient not found"

            )

        doctor = await self.doctor_repo.get_doctor_by_id(

            vital_data.doctor_id,

            hospital_id

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )

        vital_id = await IDGenerator.generate_vital_id(

            self.counter_repo

        )

        bmi = self.calculate_bmi(

            vital_data.height_cm,

            vital_data.weight_kg

        )

        vital = VitalModel(

            vital_id=vital_id,

            hospital_id=hospital_id,

            appointment_id=vital_data.appointment_id,

            patient_id=vital_data.patient_id,

            doctor_id=vital_data.doctor_id,

            height_cm=vital_data.height_cm,

            weight_kg=vital_data.weight_kg,

            bmi=bmi,

            temperature_c=vital_data.temperature_c,

            pulse_rate=vital_data.pulse_rate,

            respiratory_rate=vital_data.respiratory_rate,

            systolic_bp=vital_data.systolic_bp,

            diastolic_bp=vital_data.diastolic_bp,

            spo2=vital_data.spo2,

            blood_sugar=vital_data.blood_sugar,

            chief_complaint=vital_data.chief_complaint,

            remarks=vital_data.remarks,

            recorded_by=current_user["user_id"]

        )

        await self.vital_repo.create_vital(

            vital.model_dump()

        )

        return {

            "success": True,

            "message": "Vitals recorded successfully",

            "vital_id": vital_id

        }
        # ==========================================
    # Get By Vital ID
    # ==========================================

    async def get_by_vital_id(

        self,

        hospital_id: str,

        vital_id: str

    ):

        vital = await self.vital_repo.get_by_vital_id(

            hospital_id,

            vital_id

        )

        if not vital:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Vital record not found"

            )

        return vital

    # ==========================================
    # Patient Vital History
    # ==========================================

    async def get_patient_vitals(

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

        return await self.vital_repo.get_patient_vitals(

            hospital_id,

            patient_id

        )

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_vitals(

        self,

        hospital_id: str,

        page: int,

        limit: int,

        search: str | None,

        doctor_id: str | None,

        patient_id: str | None,

        status=None

    ):

        result= await self.vital_repo.get_all_vitals(

            hospital_id=hospital_id,

            page=page,

            limit=limit,

            search=search,

            doctor_id=doctor_id,

            patient_id=patient_id,

            status=status

        )
        return PaginatedResponse(

            data=result["items"],

            pagination=build_pagination_meta(

                page=page,

                limit=limit,

                total_records=result["total"]

            )

        )

    # ==========================================
    # Update
    # ==========================================

    async def update_vital(

        self,

        hospital_id: str,

        vital_id: str,

        update_data

    ):

        vital = await self.vital_repo.get_by_vital_id(

            hospital_id,

            vital_id

        )

        if not vital:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Vital record not found"

            )

        data = update_data.model_dump(

            exclude_unset=True

        )

        if (

            "height_cm" in data

            or

            "weight_kg" in data

        ):

            height = data.get(

                "height_cm",

                vital.get("height_cm")

            )

            weight = data.get(

                "weight_kg",

                vital.get("weight_kg")

            )

            data["bmi"] = self.calculate_bmi(

                height,

                weight

            )

        await self.vital_repo.update_vital(

            hospital_id,

            vital_id,

            data

        )

        return {

            "success": True,

            "message": "Vital updated successfully"

        }

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        vital_id: str,

        status_data

    ):

        vital = await self.vital_repo.get_by_vital_id(

            hospital_id,

            vital_id

        )

        if not vital:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Vital record not found"

            )

        await self.vital_repo.update_status(

            hospital_id,

            vital_id,

            status_data.status

        )

        return {

            "success": True,

            "message": "Vital status updated successfully"

        }

    # ==========================================
    # Delete
    # ==========================================

    async def delete_vital(

        self,

        hospital_id: str,

        vital_id: str

    ):

        vital = await self.vital_repo.get_by_vital_id(

            hospital_id,

            vital_id

        )

        if not vital:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Vital record not found"

            )

        await self.vital_repo.delete_vital(

            hospital_id,

            vital_id

        )

        return {

            "success": True,

            "message": "Vital deleted successfully"

        }