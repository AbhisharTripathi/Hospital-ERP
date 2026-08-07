from fastapi import HTTPException, status

from app.models.medicine import MedicineModel

from app.schemas.medicine import (
    MedicineCreate,
    MedicineUpdate
)

from app.utils.id_generator import IDGenerator

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)


class MedicineService:

    def __init__(
        self,
        medicine_repository,
        counter_repository
    ):

        self.medicine_repo = medicine_repository

        self.counter_repo = counter_repository

    # ==========================================
    # Create Medicine
    # ==========================================

    async def create_medicine(

        self,

        hospital_id: str,

        medicine_data: MedicineCreate,

        current_user

    ):

        # --------------------------------------
        # Check Duplicate Medicine
        # --------------------------------------

        existing = await self.medicine_repo.find_duplicate(

            hospital_id=hospital_id,

            medicine_name=medicine_data.medicine_name,

            generic_name=medicine_data.generic_name,

            strength=medicine_data.strength,

            dosage_form=medicine_data.dosage_form,

            manufacturer=medicine_data.manufacturer

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Medicine already exists"

            )

        # --------------------------------------
        # Generate Medicine ID
        # --------------------------------------

        medicine_id = await IDGenerator.generate_medicine_id(

            self.counter_repo

        )

        # --------------------------------------
        # Create Medicine Model
        # --------------------------------------

        medicine = MedicineModel(

            medicine_id=medicine_id,

            hospital_id=hospital_id,

            medicine_name=medicine_data.medicine_name,

            generic_name=medicine_data.generic_name,

            strength=medicine_data.strength,

            dosage_form=medicine_data.dosage_form,

            manufacturer=medicine_data.manufacturer,

            unit=medicine_data.unit,

            reorder_level=medicine_data.reorder_level,

            is_active=True,

            created_by=current_user["user_id"]

        )

        # --------------------------------------
        # Save
        # --------------------------------------

        await self.medicine_repo.create_medicine(

            medicine.model_dump()

        )

        return medicine

    # ==========================================
    # Get Medicine By ID
    # ==========================================

    async def get_by_medicine_id(

        self,

        hospital_id: str,

        medicine_id: str

    ):

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id,

            medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        return medicine

    # ==========================================
    # Search / Autocomplete
    # ==========================================

    async def search_medicines(

        self,

        hospital_id: str,

        search: str,

        limit: int = 10

    ):

        search = search.strip()

        if not search:

            return []

        if len(search) < 2:

            return []

        return await self.medicine_repo.search_medicines(

            hospital_id=hospital_id,

            search=search,

            limit=limit

        )

    # ==========================================
    # Get All Medicines
    # ==========================================

    async def get_all_medicines(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        dosage_form=None,

        manufacturer: str | None = None,

        is_active: bool | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        result = await self.medicine_repo.get_all_medicines(

            hospital_id=hospital_id,

            page=page,

            limit=limit,

            search=search,

            dosage_form=dosage_form,

            manufacturer=manufacturer,

            is_active=is_active,

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
    # Update Medicine
    # ==========================================

    async def update_medicine(

        self,

        hospital_id: str,

        medicine_id: str,

        medicine_data: MedicineUpdate

    ):

        # --------------------------------------
        # Medicine Exists
        # --------------------------------------

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id,

            medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        # --------------------------------------
        # Get Only Provided Fields
        # --------------------------------------

        update_data = medicine_data.model_dump(

            exclude_none=True,

            exclude_unset=True

        )

        if not update_data:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="No fields provided for update"

            )

        # --------------------------------------
        # Update
        # --------------------------------------

        await self.medicine_repo.update_medicine(

            hospital_id,

            medicine_id,

            update_data

        )

        return {

            "success": True,

            "message": "Medicine updated successfully"

        }

    # ==========================================
    # Activate / Deactivate
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        medicine_id: str,

        is_active: bool

    ):

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id,

            medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        if medicine["is_active"] == is_active:

            state = "active" if is_active else "inactive"

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail=f"Medicine is already {state}"

            )

        await self.medicine_repo.update_status(

            hospital_id,

            medicine_id,

            is_active

        )

        return {

            "success": True,

            "message": (

                "Medicine activated successfully"

                if is_active

                else

                "Medicine deactivated successfully"

            )

        }