from datetime import datetime,timezone
import bcrypt

from app.models.patient import PatientModel
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientSearch
)
from app.repositories.patient import PatientRepository
from app.utils.id_generator import IDGenerator
from app.models.patient import PatientStatus

class PatientServices:

    def __init__(
        self,
        patient_repository,
        counter_repository
    ):
        self.patient_repo: PatientRepository = patient_repository
        self.counter_repo = counter_repository

    async def create_patient(
        self,
        patient: PatientCreate
    ):

        # Duplicate phone check
        existing_patient = await self.patient_repo.get_by_phone(
            patient.phone
        )

        if existing_patient:
            raise ValueError(
                "Patient already exists with this phone number"
            )

        # Generate Patient ID
        patient_id = await IDGenerator.generate_patient_id(
            self.counter_repo
        )

        # Password handling
        if patient.password:
            raw_password = patient.password
        else:
            raw_password = patient.dob.strftime(
                "%d%m%Y"
            )

        hashed_password = bcrypt.hashpw(
            raw_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Schema -> Dict
        patient_data = patient.model_dump(
            exclude={"password"}
        )

        # Extra fields
        patient_data["patient_id"] = patient_id
        patient_data["password"] = hashed_password

        # Final validation through model
        patient_model = PatientModel(
            **patient_data
        )

        inserted_id = await self.patient_repo.create_patient(
            patient_model.model_dump()
        )

        return {
            "patient_id": patient_id,
            "inserted_id": str(inserted_id)
        }

    async def get_patient_by_id(
        self,
        patient_id: str
    ):

        patient = await self.patient_repo.get_by_patient_id(
            patient_id
        )

        if not patient:
            raise ValueError(
                "Patient not found"
            )

        return patient

    async def get_all_patients(
        self,
        limit
    ):

        return await self.patient_repo.get_all_patients(
            limit
        )

    async def search_patients(
        self,
        search: PatientSearch
    ):

        filters = {}

        if search.patient_id:
            filters["patient_id"] = search.patient_id

        if search.phone:
            filters["phone"] = search.phone

        if search.first_name:
            filters["first_name"] = search.first_name

        if search.address:
            filters["address"] = search.address

        return await self.patient_repo.search_patients(
            filters
        )

    async def update_patient(
        self,
        patient_id: str,
        patient_update: PatientUpdate
    ):

        patient = await self.patient_repo.get_by_patient_id(
            patient_id
        )

        if not patient:
            raise ValueError(
                "Patient not found"
            )

        update_data = patient_update.model_dump(
            exclude_unset=True
        )

        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.patient_repo.update_by_patient_id(
            patient_id,
            update_data
        )

        return {
            "modified_count": result.modified_count
        }

    async def deactivate_patient(
        self,
        patient_id: str
    ):

        patient = await self.patient_repo.get_by_patient_id(
            patient_id
        )

        if not patient:
            raise ValueError(
                "Patient not found"
            )

        result = await self.patient_repo.update_by_patient_id(
            patient_id,
            {
                "status": PatientStatus.INACTIVE,
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return {
            "modified_count": result.modified_count
        }