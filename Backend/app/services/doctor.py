from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.doctor import (
    DoctorModel,
    DoctorStatus
)

from app.models.user import (
    UserModel,
    UserRole
)

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate
)

from app.repositories.doctor import DoctorRepository
from app.repositories.user import UserRepository

from app.utils.id_generator import IDGenerator

from app.core.security import hash_password


class DoctorService:

    def __init__(
        self,
        doctor_repository,
        user_repository,
        counter_repository
    ):
        self.doctor_repo: DoctorRepository = doctor_repository
        self.user_repo: UserRepository = user_repository
        self.counter_repo = counter_repository

    async def create_doctor(
        self,
        doctor: DoctorCreate
    ):

        existing_user = await self.user_repo.get_by_email(
            doctor.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

        user_id = await IDGenerator.generate_user_id(
            self.counter_repo
        )

        doctor_id = await IDGenerator.generate_doctor_id(
            self.counter_repo
        )

        hashed_password = hash_password(
            doctor.password
        )

        user_model = UserModel(
            user_id=user_id,
            username=doctor.email.split("@")[0],
            email=doctor.email,
            password=hashed_password,
            role=UserRole.DOCTOR
        )

        await self.user_repo.create_user(
            user_model.model_dump(mode="json")
        )

        doctor_data = doctor.model_dump(
            exclude={"password"}
        )

        doctor_data.update(
            {
                "doctor_id": doctor_id,
                "user_id": user_id
            }
        )

        doctor_model = DoctorModel(
            **doctor_data
        )

        await self.doctor_repo.create_doctor(
            doctor_model.model_dump(mode="json")
        )

        return {
            "doctor_id": doctor_id,
            "user_id": user_id
        }

    async def get_doctor_by_id(
        self,
        doctor_id: str
    ):

        doctor = await self.doctor_repo.get_doctor_by_id(
            doctor_id
        )

        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

        return doctor

    async def get_all_doctors(
        self,
        limit: int = 100
    ):

        return await self.doctor_repo.get_all_doctors(
            limit
        )

    async def update_doctor(
        self,
        doctor_id: str,
        doctor_update: DoctorUpdate
    ):

        doctor = await self.get_doctor_by_id(
            doctor_id
        )

        update_data = doctor_update.model_dump(
            exclude_unset=True,
            mode="json"
        )

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        result = await self.doctor_repo.update_by_doctor_id(
            doctor_id,
            update_data
        )

        return {
            "modified_count": result.modified_count
        }

    async def deactivate_doctor(
        self,
        doctor_id: str
    ):

        doctor = await self.get_doctor_by_id(
            doctor_id
        )

        result = await self.doctor_repo.update_by_doctor_id(
            doctor_id,
            {
                "status": DoctorStatus.INACTIVE,
                "updated_at": datetime.now(
                    timezone.utc
                )
            }
        )

        return {
            "modified_count": result.modified_count
        }