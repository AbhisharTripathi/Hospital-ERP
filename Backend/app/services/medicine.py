from fastapi import HTTPException, status

from app.models.medicine import MedicineModel

from app.schemas.medicine import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse
)

from app.repositories.medicine import (
    MedicineRepository
)

from app.repositories.counters import (
    CountersRepository
)

from app.utils.id_generator import (
    IDGenerator
)

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)


class MedicineService:

    def __init__(
        self,
        medicine_repository: MedicineRepository,
        counter_repository: CountersRepository
    ):

        self.medicine_repo = medicine_repository
        self.counter_repo = counter_repository

    # --------------------------------------------------
    # Response Builder
    # --------------------------------------------------

    def _build_response(
        self,
        medicine: dict
    ):

        return MedicineResponse(

            medicine_id=medicine["medicine_id"],

            hospital_id=medicine["hospital_id"],

            medicine_name=medicine["medicine_name"],

            generic_name=medicine.get("generic_name"),

            strength=medicine["strength"],

            dosage_form=medicine["dosage_form"],

            manufacturer=medicine.get("manufacturer"),

            unit=medicine["unit"],

            reorder_level=medicine["reorder_level"],

            is_active=medicine["is_active"],

            created_by=medicine["created_by"],

            created_at=medicine["created_at"],

            updated_at=medicine["updated_at"]

        )

    # --------------------------------------------------
    # Create Medicine
    # --------------------------------------------------

    async def create_medicine(
        self,
        current_user,
        medicine_data: MedicineCreate
    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Duplicate Validation ----------------

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

        # ---------------- Medicine ID ----------------

        medicine_id = await IDGenerator.generate_medicine_id(

            self.counter_repo

        )

        # ---------------- Model ----------------

        medicine_model = MedicineModel(

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

        # ---------------- Create ----------------

        await self.medicine_repo.create_medicine(

            medicine_model.model_dump(mode="json")

        )

        # ---------------- Response ----------------

        return self._build_response(

            medicine_model.model_dump(mode="json")

        )

    # --------------------------------------------------
    # Search / Autocomplete
    # --------------------------------------------------

    async def search_medicines(
        self,
        current_user,
        search: str,
        limit: int = 10
    ):

        hospital_id = current_user["hospital_id"]

        search = search.strip()

        if not search:

            return []

        if len(search) < 2:

            return []

        medicines = await self.medicine_repo.search_medicines(

            hospital_id=hospital_id,

            search=search,

            limit=limit

        )

        return [

            self._build_response(item)

            for item in medicines

        ]

    # --------------------------------------------------
    # Get All Medicines
    # --------------------------------------------------

    async def get_all_medicines(
        self,
        current_user,
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

            hospital_id=current_user["hospital_id"],

            page=page,

            limit=limit,

            search=search,

            dosage_form=dosage_form,

            manufacturer=manufacturer,

            is_active=is_active,

            sort_by=sort_by,

            sort_order=sort_order

        )

        medicines = [

            self._build_response(item)

            for item in result["items"]

        ]

        return {

            "items": medicines,

            "total": result["total"],

            "page": page,

            "limit": limit,

            "total_pages": (

                result["total"] + limit - 1

            ) // limit

        }
        # --------------------------------------------------
    # Get Medicine By ID
    # --------------------------------------------------

    async def get_medicine_by_id(
        self,
        current_user,
        medicine_id: str
    ):

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        return self._build_response(
            medicine
        )

    # --------------------------------------------------
    # Update Medicine
    # --------------------------------------------------

    async def update_medicine(
        self,
        current_user,
        medicine_id: str,
        medicine_data: MedicineUpdate
    ):

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        # ---------------- Update Data ----------------

        update_data = medicine_data.model_dump(

            exclude_unset=True,

            mode="json"

        )

        if not update_data:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Nothing to update"

            )

        # ---------------- Update ----------------

        await self.medicine_repo.update_medicine(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id,

            update_data=update_data

        )

        # ---------------- Get Updated Medicine ----------------

        updated = await self.medicine_repo.get_by_medicine_id(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id

        )

        return self._build_response(
            updated
        )

    # --------------------------------------------------
    # Update Medicine Status
    # --------------------------------------------------

    async def update_status(
        self,
        current_user,
        medicine_id: str,
        is_active: bool
    ):

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        if medicine["is_active"] == is_active:

            state = (
                "active"
                if is_active
                else
                "inactive"
            )

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail=f"Medicine is already {state}"

            )

        # ---------------- Update Status ----------------

        await self.medicine_repo.update_status(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id,

            is_active=is_active

        )

        # ---------------- Get Updated Medicine ----------------

        updated = await self.medicine_repo.get_by_medicine_id(

            hospital_id=current_user["hospital_id"],

            medicine_id=medicine_id

        )

        return self._build_response(
            updated
        )
    