from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.models.batch import (
    BatchModel,
    BatchStatus
)

from app.schemas.batch import (
    BatchCreate,
    BatchUpdate,
    BatchResponse
)

from app.repositories.batch import (
    BatchRepository
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


class BatchService:

    def __init__(
        self,
        batch_repository: BatchRepository,
        medicine_repository: MedicineRepository,
        counter_repository: CountersRepository
    ):

        self.batch_repo = batch_repository
        self.medicine_repo = medicine_repository
        self.counter_repo = counter_repository

    # --------------------------------------------------
    # Response Builder
    # --------------------------------------------------

    def _build_response(
        self,
        batch: dict
    ):

        return BatchResponse(

            batch_id=batch["batch_id"],

            hospital_id=batch["hospital_id"],

            medicine_id=batch["medicine_id"],

            batch_number=batch["batch_number"],

            expiry_date=batch["expiry_date"],

            purchase_price=batch["purchase_price"],

            unit=batch["unit"],

            status=batch["status"],

            
            created_at=batch.get("created_at") or datetime.now(timezone.utc),
            updated_at=batch.get("updated_at") or datetime.now(timezone.utc),

        )

    # --------------------------------------------------
    # Create Batch
    # --------------------------------------------------

    async def create_batch(
        self,
        current_user,
        batch_data: BatchCreate
    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Medicine Validation ----------------

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=hospital_id,

            medicine_id=batch_data.medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        # ---------------- Active Medicine Check ----------------

        if not medicine["is_active"]:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Medicine is inactive"

            )

        # ---------------- Duplicate Batch Check ----------------

        existing = await self.batch_repo.find_by_medicine_and_batch(

            hospital_id=hospital_id,

            medicine_id=batch_data.medicine_id,

            batch_number=batch_data.batch_number

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Batch already exists for this medicine"

            )

        # ---------------- Batch ID ----------------

        batch_id = await IDGenerator.generate_batch_id(

            self.counter_repo

        )

        # ---------------- Create Model ----------------

        batch_model = BatchModel(

            batch_id=batch_id,

            hospital_id=hospital_id,

            medicine_id=batch_data.medicine_id,

            batch_number=batch_data.batch_number,

            expiry_date=batch_data.expiry_date,

            purchase_price=batch_data.purchase_price,

            unit=batch_data.unit,

            status=BatchStatus.ACTIVE

        )

        # ---------------- Create ----------------

        await self.batch_repo.create_batch(

            batch_model.model_dump(
                mode="json"
            )

        )

        # ---------------- Response ----------------

        return self._build_response(

            batch_model.model_dump(
                mode="json"
            )

        )

    # --------------------------------------------------
    # Get Batch By ID
    # --------------------------------------------------

    async def get_batch_by_id(

        self,
        current_user,
        batch_id: str

    ):

        hospital_id = current_user["hospital_id"]

        batch = await self.batch_repo.get_by_batch_id(

            hospital_id=hospital_id,

            batch_id=batch_id

        )

        if not batch:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Batch not found"

            )

        return self._build_response(batch)

    # --------------------------------------------------
    # Get Batches By Medicine
    # --------------------------------------------------

    async def get_batches_by_medicine(

        self,
        current_user,
        medicine_id: str

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Medicine Validation ----------------

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=hospital_id,

            medicine_id=medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        batches = await self.batch_repo.get_by_medicine(

            hospital_id=hospital_id,

            medicine_id=medicine_id

        )

        return [

            self._build_response(batch)

            for batch in batches

        ]

    # --------------------------------------------------
    # Get All Batches
    # --------------------------------------------------

    async def get_all_batches(

        self,
        current_user,
        page: int = 1,
        limit: int = 20,
        medicine_id: str | None = None,
        status: BatchStatus | None = None,
        sort_by: str = "expiry_date",
        sort_order: int = 1

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Medicine Validation ----------------

        if medicine_id:

            medicine = await self.medicine_repo.get_by_medicine_id(

                hospital_id=hospital_id,

                medicine_id=medicine_id

            )

            if not medicine:

                raise HTTPException(

                    status_code=status.HTTP_404_NOT_FOUND,

                    detail="Medicine not found"

                )

        result = await self.batch_repo.get_all_batches(

            hospital_id=hospital_id,

            page=page,

            limit=limit,

            medicine_id=medicine_id,

            status=status,

            sort_by=sort_by,

            sort_order=sort_order

        )

        batches = [

            self._build_response(batch)

            for batch in result["items"]

        ]

        return {

            "items": batches,

            "total": result["total"],

            "page": page,

            "limit": limit,

            "total_pages": (

                result["total"] + limit - 1
            ) // limit

        }

    # --------------------------------------------------
    # Update Batch
    # --------------------------------------------------

    async def update_batch(

        self,
        current_user,
        batch_id: str,
        batch_data: BatchUpdate

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Batch Exists ----------------

        batch = await self.batch_repo.get_by_batch_id(

            hospital_id=hospital_id,

            batch_id=batch_id

        )

        if not batch:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Batch not found"

            )

        # ---------------- Update Data ----------------

        update_data = batch_data.model_dump(

            exclude_unset=True,

            exclude_none=True,

            mode="json"

        )

        if not update_data:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Nothing to update"

            )

        # ---------------- Update ----------------

        await self.batch_repo.update_batch(

            hospital_id=hospital_id,

            batch_id=batch_id,

            update_data=update_data

        )

        # ---------------- Get Updated ----------------

        updated = await self.batch_repo.get_by_batch_id(

            hospital_id=hospital_id,

            batch_id=batch_id

        )

        return self._build_response(updated)

    # --------------------------------------------------
    # Get Expired Batches
    # --------------------------------------------------

    async def get_expired_batches(

        self,
        current_user,
        today

    ):

        hospital_id = current_user["hospital_id"]

        batches = await self.batch_repo.get_expired_batches(

            hospital_id=hospital_id,

            today=today

        )

        return [

            self._build_response(batch)

            for batch in batches

        ]