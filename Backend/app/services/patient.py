


from app.schemas.pagination import PaginatedResponse
from datetime import datetime, timezone
import math
import bcrypt

from fastapi import HTTPException, status

from app.models.patient import PatientModel, PatientStatus
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientSearch,
    PatientResponse
)
# from app.schemas.pagination import PaginatedResponse,build_pagination_meta
from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)

from app.repositories.patient import PatientRepository
from app.utils.id_generator import IDGenerator


class PatientServices:

    ALLOWED_SORT_FIELDS = {
        "created_at",
        "updated_at",
        "first_name",
        "patient_id",
        "dob",
        "status"
    }

    def __init__(
        self,
        patient_repository,
        counter_repository
    ):
        self.patient_repo: PatientRepository = patient_repository
        self.counter_repo = counter_repository

    async def create_patient(
        self,
        patient: PatientCreate,
       
        current_user
    ):
        if isinstance(current_user, dict):
            hospital_id = current_user.get("hospital_id")
        else:
            hospital_id = getattr(current_user, "hospital_id", None)

        if not hospital_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hospital ID is required for creating a patient."
            )
        existing_patient = await self.patient_repo.get_by_phone(
            hospital_id=current_user["hospital_id"],
            phone=patient.phone
        )

        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Patient already exists with this phone number."
            )

        patient_id = await IDGenerator.generate_patient_id(
            self.counter_repo
        )

        if patient.password:
            raw_password = patient.password
        else:
            raw_password = patient.dob.strftime("%d%m%Y")

        hashed_password = bcrypt.hashpw(
            raw_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        patient_data = patient.model_dump(
            exclude={"password"}
        )

        patient_data["patient_id"] = patient_id
        patient_data["hospital_id"] = current_user["hospital_id"]
        patient_data["password"] = hashed_password
        # patient_data["hospital_id"] = hospital_id
        patient_model = PatientModel(
            **patient_data
        )

        inserted_id = await self.patient_repo.create_patient(
            patient_model.model_dump(mode="json")
        )

        return {
            "patient_id": patient_id,
            "inserted_id": str(inserted_id)
        }

    async def get_all_patients(
        self,
        current_user,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        status: PatientStatus | None = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):

        if sort_by not in self.ALLOWED_SORT_FIELDS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sort field. Allowed fields: {', '.join(self.ALLOWED_SORT_FIELDS)}"
            )

        if sort_order not in (1, -1):
            raise HTTPException(
                status_code=400,
                detail="sort_order must be either 1 or -1."
            )

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        result = await self.patient_repo.get_all_patients(
            hospital_id=current_user["hospital_id"],
            page=page,
            limit=limit,
            search=search,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )

        response = []

        for patient in result["items"]:

            response.append(

                PatientResponse(
                    hospital_id=patient["hospital_id"],
                    patient_id=patient["patient_id"],
                    
                    first_name=patient["first_name"],
                    last_name=patient.get("last_name"),

                    gender=patient["gender"],
                    dob=patient["dob"],

                    phone=patient["phone"],
                    email=patient.get("email"),

                    blood_group=patient.get("blood_group"),

                    address=patient.get("address"),

                    emergency_contact_name=patient.get(
                        "emergency_contact_name"
                    ),
                    emergency_contact_phone=patient.get(
                        "emergency_contact_phone"
                    ),

                    status=patient["status"],

                    notes=patient.get("notes"),

                    created_at=patient["created_at"],
                    updated_at=patient["updated_at"]
                )

            )

        return PaginatedResponse[PatientResponse](

            data=response,

            pagination=build_pagination_meta(
                page=page,
                limit=limit,
                total_records=result["total"]
            )

        )
    async def get_patient_by_id(
        self,
        current_user,
        patient_id: str
    ):

        patient = await self.patient_repo.get_patient_by_id(
            hospital_id=current_user["hospital_id"],
            patient_id=patient_id
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found."
            )

        return PatientResponse(
            hospital_id=patient["hospital_id"],
            patient_id=patient["patient_id"],

            first_name=patient["first_name"],
            last_name=patient.get("last_name"),

            gender=patient["gender"],
            dob=patient["dob"],

            phone=patient["phone"],
            email=patient.get("email"),

            blood_group=patient.get("blood_group"),

            address=patient.get("address"),

            emergency_contact_name=patient.get(
                "emergency_contact_name"
            ),
            emergency_contact_phone=patient.get(
                "emergency_contact_phone"
            ),

            status=patient["status"],

            notes=patient.get("notes"),

            created_at=patient["created_at"],
            updated_at=patient["updated_at"]

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

        patients = await self.patient_repo.search_patients(
            filters
        )

        response = []

        for patient in patients:

            response.append(

                PatientResponse(
                    hospital_id=patient["hospital_id"],
                    patient_id=patient["patient_id"],

                    first_name=patient["first_name"],
                    last_name=patient.get("last_name"),

                    gender=patient["gender"],
                    dob=patient["dob"],

                    phone=patient["phone"],
                    email=patient.get("email"),

                    blood_group=patient.get("blood_group"),

                    address=patient.get("address"),

                    emergency_contact_name=patient.get(
                        "emergency_contact_name"
                    ),
                    emergency_contact_phone=patient.get(
                        "emergency_contact_phone"
                    ),

                    status=patient["status"],

                    notes=patient.get("notes"),

                    created_at=patient["created_at"],
                    updated_at=patient["updated_at"]

                )

            )

        return response

    async def update_patient(
        self,
        patient_id: str,
        current_user,
        patient_update: PatientUpdate
    ):

        patient = await self.patient_repo.get_patient_by_id(
            hospital_id=current_user["hospital_id"],
            patient_id=patient_id
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found."
            )

        update_data = patient_update.model_dump(
            exclude_unset=True,
            mode="json"
        )

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        result = await self.patient_repo.update_by_patient_id(
            hospital_id=current_user["hospital_id"],
            patient_id=patient_id,
            updated_data=update_data    
        )

        return {
            "modified_count": result.modified_count
        }

    async def deactivate_patient(
        self,
        current_user,
        patient_id: str
    ):

        patient = await self.patient_repo.get_patient_by_id(
            hospital_id=current_user["hospital_id"],
            
            patient_id=patient_id    
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found."
            )

        result = await self.patient_repo.update_by_patient_id(

            hospital_id=current_user["hospital_id"],

            patient_id=patient_id,

            updated_data={

                "status": PatientStatus.INACTIVE,
                "updated_at": datetime.now(timezone.utc)

            }

        )

        return {
            "modified_count": result.modified_count
        }