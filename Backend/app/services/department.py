from fastapi import HTTPException, status

from app.models.department import DepartmentModel
from app.repositories.department import DepartmentRepository
from app.repositories.counters import CountersRepository
from datetime import datetime,timezone
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    UpdateDepartmentStatus
)

from app.utils.id_generator import IDGenerator
from app.constants.default_department import DEFAULT_DEPARTMENTS

class DepartmentService:

    def __init__(
        self,
        department_repository: DepartmentRepository,
        counter_repository: CountersRepository
    ):

        self.department_repo = department_repository
        self.counter_repo = counter_repository

    async def create_department(
        self,
        current_user,
        department_data: DepartmentCreate
    ):
        existing_department = await self.department_repo.get_by_name(
            hospital_id=current_user["hospital_id"],
            name=department_data.name
        )

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department already exists"
            )
        
        existing_code = await self.department_repo.get_by_code(
            hospital_id=current_user["hospital_id"],
            code=department_data.code
        )

        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department code already exists"
            )
        
        department_id = await IDGenerator.generate_department_id(
            self.counter_repo
        )

        department_model = DepartmentModel(

            department_id=department_id,

            hospital_id=current_user["hospital_id"],

            name=department_data.name,

            code=department_data.code,

            description=department_data.description,

            created_by=current_user["user_id"]
        )

        await self.department_repo.create_department(
            department_model.model_dump(mode="json")
        )

        return DepartmentResponse(

            department_id=department_model.department_id,

            hospital_id=department_model.hospital_id,

            name=department_model.name,

            code=department_model.code,

            description=department_model.description,

            head_doctor_id=department_model.head_doctor_id,

            is_active=department_model.is_active
        )
    
    async def create_default_departments(
        self,
        hospital_id: str,
        created_by: str
    ):

        departments = []

        for dept in DEFAULT_DEPARTMENTS:

            department_id = await IDGenerator.generate_department_id(
                self.counter_repo
            )

            department = DepartmentModel(

                department_id=department_id,

                hospital_id=hospital_id,

                name=dept["name"],

                code=dept["code"],

                description=dept.get("description"), 

                created_by=created_by

            )

            departments.append(
                department.model_dump(mode="json")
            )

        await self.department_repo.create_many_departments(
            departments
        )

    async def get_all_departments(
        self,
        current_user
    ):

        departments = await self.department_repo.get_all_departments(
            hospital_id=current_user["hospital_id"]
        )

        return [

            DepartmentResponse(

                department_id=department["department_id"],

                hospital_id=department["hospital_id"],

                name=department["name"],

                code=department["code"],

                description=department.get("description"),

                head_doctor_id=department.get(
                    "head_doctor_id"
                ),

                is_active=department["is_active"]

            )

            for department in departments

        ]

    async def get_department_by_id(
        self,
        current_user,
        department_id: str
    ):

        department = await self.department_repo.get_by_department_id(
            department_id=department_id,
            hospital_id=current_user["hospital_id"]
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        return DepartmentResponse(
            department_id=department["department_id"],
            hospital_id=department["hospital_id"],
            name=department["name"],
            code=department["code"],
            description=department.get("description"),
            head_doctor_id=department.get("head_doctor_id"),
            is_active=department["is_active"]
        )
    async def update_department(
        self,
        current_user,
        department_id: str,
        department_data: DepartmentUpdate
    ):

        department = await self.department_repo.get_by_department_id(
            department_id=department_id,
            hospital_id=current_user["hospital_id"]
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        update_fields = department_data.model_dump(
            exclude_unset=True
        )

        update_data = {}

        if "name" in update_fields:

            existing = await self.department_repo.get_by_name(
                hospital_id=current_user["hospital_id"],
                name=update_fields["name"]
            )

            if (
                existing
                and existing["department_id"] != department_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Department name already exists"
                )

            update_data["name"] = update_fields["name"]

        if "description" in update_fields:
            update_data["description"] = update_fields["description"]

        if "head_doctor_id" in update_fields:
            update_data["head_doctor_id"] = update_fields["head_doctor_id"]

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        await self.department_repo.update_department(
            department_id=department_id,
            hospital_id=current_user["hospital_id"],
            update_data=update_data
        )

        updated_department = await self.department_repo.get_by_department_id(
            department_id=department_id,
            hospital_id=current_user["hospital_id"]
        )

        return DepartmentResponse(

            department_id=updated_department["department_id"],

            hospital_id=updated_department["hospital_id"],

            name=updated_department["name"],

            code=updated_department["code"],

            description=updated_department.get("description"),

            head_doctor_id=updated_department.get(
                "head_doctor_id"
            ),

            is_active=updated_department["is_active"]
        )
    

    async def update_department_status(
        self,
        current_user,
        department_id: str,
        status_data: UpdateDepartmentStatus
    ):

        department = await self.department_repo.get_by_department_id(
            department_id=department_id,
            hospital_id=current_user["hospital_id"]
        )
        return department