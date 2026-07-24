from fastapi import (
    HTTPException,
    status
)

from app.models.pharmacy import (
    PharmacyModel,
    PharmacyMedicine,
    PharmacyStatus
)

from app.schemas.pharmacy import (
    PharmacyCreate
)

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)

from app.utils.id_generator import (
    IDGenerator
)


class PharmacyService:

    def __init__(

        self,

        pharmacy_repository,

        prescription_repository,

        appointment_repository,

        patient_repository,

        doctor_repository,

        counter_repository

    ):

        self.pharmacy_repo = pharmacy_repository

        self.prescription_repo = prescription_repository

        self.appointment_repo = appointment_repository

        self.patient_repo = patient_repository

        self.doctor_repo = doctor_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Create Pharmacy Order
    # ==========================================

    async def create_pharmacy(

        self,

        hospital_id: str,

        pharmacy_data: PharmacyCreate,

        current_user

    ):

        # --------------------------------------
        # Prescription Exists
        # --------------------------------------

        prescription = await self.prescription_repo.get_by_prescription_id(

            hospital_id,

            pharmacy_data.prescription_id

        )

        if not prescription:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Prescription not found"

            )

        # --------------------------------------
        # Prevent Duplicate Pharmacy Order
        # --------------------------------------

        existing = await self.pharmacy_repo.get_by_prescription_id(

            hospital_id,

            pharmacy_data.prescription_id

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Pharmacy order already exists"

            )

        # --------------------------------------
        # Appointment Exists
        # --------------------------------------

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id,

            prescription["appointment_id"]

        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        # --------------------------------------
        # Patient Exists
        # --------------------------------------

        patient = await self.patient_repo.get_patient_by_id(

            hospital_id,

            prescription["patient_id"]

        )

        if not patient:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Patient not found"

            )

        # --------------------------------------
        # Doctor Exists
        # --------------------------------------

        doctor = await self.doctor_repo.get_doctor_by_id(

            prescription["doctor_id"],

            hospital_id

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )

        # --------------------------------------
        # Generate Pharmacy ID
        # --------------------------------------

        pharmacy_id = await IDGenerator.generate_pharmacy_id(

            self.counter_repo

        )

        medicines = []

        for medicine in prescription.get("medicines", []):
            # Fallback system for key safety (KeyError se bachne ke liye)
            qty = (
                medicine.get("quantity") 
                or medicine.get("prescribed_quantity") 
                or medicine.get("qty") 
                or 1
            )

            medicines.append(

                PharmacyMedicine(

                    medicine_name=medicine["medicine_name"],

                    dosage=medicine["dosage"],

                    frequency=medicine["frequency"],

                    duration=medicine["duration"],

                    timing=medicine["timing"],

                    prescribed_quantity=int(qty),

                    dispensed_quantity=0,

                    remarks=None

                )

            )

        pharmacy = PharmacyModel(

            pharmacy_id=pharmacy_id,

            hospital_id=hospital_id,

            prescription_id=prescription["prescription_id"],

            appointment_id=prescription["appointment_id"],

            patient_id=prescription["patient_id"],

            doctor_id=prescription["doctor_id"],

            pharmacist_id=None,

            medicines=medicines,

            status=PharmacyStatus.PENDING,

            created_by=current_user["user_id"]

        )

        await self.pharmacy_repo.create_pharmacy(

            pharmacy.model_dump()

        )

        return {

            "success": True,

            "message": "Pharmacy order created successfully",

            "pharmacy_id": pharmacy_id

        }
        # ==========================================
    # Get Pharmacy By ID
    # ==========================================

    async def get_by_pharmacy_id(

        self,

        hospital_id: str,

        pharmacy_id: str

    ):

        pharmacy = await self.pharmacy_repo.get_by_pharmacy_id(

            hospital_id,

            pharmacy_id

        )

        if not pharmacy:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Pharmacy order not found"

            )

        return pharmacy

    # ==========================================
    # Get Patient Pharmacy History
    # ==========================================

    async def get_patient_pharmacy(

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

        return await self.pharmacy_repo.get_by_patient(

            hospital_id,

            patient_id

        )

    # ==========================================
    # Get All Pharmacy Orders
    # ==========================================

    async def get_all_pharmacy(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        patient_id: str | None = None,

        doctor_id: str | None = None,

        pharmacist_id: str | None = None,

        status: PharmacyStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        result = await self.pharmacy_repo.get_all_pharmacy(

            hospital_id=hospital_id,

            page=page,

            limit=limit,

            search=search,

            patient_id=patient_id,

            doctor_id=doctor_id,

            pharmacist_id=pharmacist_id,

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
    # Update Pharmacy
    # ==========================================

    async def update_pharmacy(

        self,

        hospital_id: str,

        pharmacy_id: str,

        pharmacy_data

    ):

        pharmacy = await self.pharmacy_repo.get_by_pharmacy_id(

            hospital_id,

            pharmacy_id

        )

        if not pharmacy:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Pharmacy order not found"

            )

        update_data = pharmacy_data.model_dump(

            exclude_none=True,

            exclude_unset=True

        )

        await self.pharmacy_repo.update_pharmacy(

            hospital_id,

            pharmacy_id,

            update_data

        )

        return {

            "success": True,

            "message": "Pharmacy updated successfully"

        }

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        pharmacy_id: str,

        status_data,

        current_user

    ):

        pharmacy = await self.pharmacy_repo.get_by_pharmacy_id(

            hospital_id,

            pharmacy_id

        )

        if not pharmacy:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Pharmacy order not found"

            )

        await self.pharmacy_repo.update_status(

            hospital_id,

            pharmacy_id,

            status_data.status,

            current_user["user_id"]

        )

        return {

            "success": True,

            "message": "Pharmacy status updated successfully"

        }

    # ==========================================
    # Delete Pharmacy
    # ==========================================

    async def delete_pharmacy(

        self,

        hospital_id: str,

        pharmacy_id: str

    ):

        pharmacy = await self.pharmacy_repo.get_by_pharmacy_id(

            hospital_id,

            pharmacy_id

        )

        if not pharmacy:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Pharmacy order not found"

            )

        await self.pharmacy_repo.delete_pharmacy(

            hospital_id,

            pharmacy_id

        )

        return {

            "success": True,

            "message": "Pharmacy order deleted successfully"

        }