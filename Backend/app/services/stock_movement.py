from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.stock_movement import (
    StockMovementModel,
    StockMovementType
)

from app.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse
)

from app.repositories.stock_movement import (
    StockMovementRepository
)

from app.repositories.stock import (
    StockRepository
)

from app.utils.id_generator import (
    IDGenerator
)

from app.repositories.counters import (
    CountersRepository
)


class StockMovementService:

    def __init__(
        self,
        stock_movement_repository: StockMovementRepository,
        stock_repository: StockRepository,
        counter_repository: CountersRepository
    ):

        self.movement_repo = stock_movement_repository
        self.stock_repo = stock_repository
        self.counter_repo = counter_repository

    # ==========================================
    # Response Builder
    # ==========================================
    def _build_response(self, movement: dict) -> StockMovementResponse:
        now = datetime.now(timezone.utc)

        return StockMovementResponse(
            movement_id=movement.get("movement_id") or str(movement.get("_id", "")),
            hospital_id=movement.get("hospital_id"),
            stock_id=movement.get("stock_id"),
            medicine_id=movement.get("medicine_id"),
            batch_id=movement.get("batch_id"),
            movement_type=movement.get("movement_type"),
            quantity=movement.get("quantity", 0),
            reference_type=movement.get("reference_type"),
            reference_id=movement.get("reference_id"),
            reason=movement.get("reason"),
            created_by=movement.get("created_by"),
            created_at=movement.get("created_at") or movement.get("createdAt") or now,
        )
    

    # ==========================================
    # Create Movement
    # ==========================================

    async def create_movement(

        self,
        current_user,
        movement_data: StockMovementCreate

    ):

        hospital_id = current_user["hospital_id"]

        # --------------------------------------
        # Stock Validation
        # --------------------------------------

        stock = await self.stock_repo.get_by_stock_id(

            hospital_id=hospital_id,

            stock_id=movement_data.stock_id

        )

        if not stock:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Stock not found"

            )

        # --------------------------------------
        # Generate Movement ID
        # --------------------------------------

        movement_id = await IDGenerator.generate_stock_movement_id(

            self.counter_repo

        )

        # --------------------------------------
        # Model
        # --------------------------------------

        movement_model = StockMovementModel(

            movement_id=movement_id,

            hospital_id=hospital_id,

            stock_id=stock["stock_id"],

            medicine_id=stock["medicine_id"],

            batch_id=stock["batch_id"],

            movement_type=movement_data.movement_type,

            quantity=movement_data.quantity,

            reference_type=movement_data.reference_type,

            reference_id=movement_data.reference_id,

            reason=movement_data.reason,

            created_by=current_user["user_id"]

        )

        # --------------------------------------
        # Create Movement
        # --------------------------------------

        await self.movement_repo.create_movement(

            movement_model.model_dump(
                mode="json"
            )

        )

        # --------------------------------------
        # Response
        # --------------------------------------

        return self._build_response(

            movement_model.model_dump(
                mode="json"
            )

        )

    # ==========================================
    # Get Movement By ID
    # ==========================================

    async def get_movement_by_id(

        self,
        current_user,
        movement_id: str

    ):

        movement = await self.movement_repo.get_by_movement_id(

            hospital_id=current_user["hospital_id"],

            movement_id=movement_id

        )

        if not movement:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Stock movement not found"

            )

        return self._build_response(
            movement
        )

    # ==========================================
    # Get Stock History
    # ==========================================

    async def get_stock_history(

        self,
        current_user,
        stock_id: str

    ):

        hospital_id = current_user["hospital_id"]

        # --------------------------------------
        # Stock Validation
        # --------------------------------------

        stock = await self.stock_repo.get_by_stock_id(

            hospital_id=hospital_id,

            stock_id=stock_id

        )

        if not stock:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Stock not found"

            )

        movements = await self.movement_repo.get_by_stock_id(

            hospital_id=hospital_id,

            stock_id=stock_id

        )

        return [

            self._build_response(movement)

            for movement in movements

        ]

    # ==========================================
    # Get Movements By Reference
    # ==========================================

    async def get_by_reference(

        self,
        current_user,
        reference_type: str,
        reference_id: str

    ):

        movements = await self.movement_repo.get_by_reference(

            hospital_id=current_user["hospital_id"],

            reference_type=reference_type,

            reference_id=reference_id

        )

        return [

            self._build_response(movement)

            for movement in movements

        ]

    # ==========================================
    # Get All Movements
    # ==========================================

    async def get_all_movements(

        self,
        current_user,

        page: int = 1,

        limit: int = 20,

        stock_id: str | None = None,

        medicine_id: str | None = None,

        batch_id: str | None = None,

        movement_type: StockMovementType | None = None

    ):

        result = await self.movement_repo.get_all_movements(

            hospital_id=current_user["hospital_id"],

            page=page,

            limit=limit,

            stock_id=stock_id,

            medicine_id=medicine_id,

            batch_id=batch_id,

            movement_type=movement_type

        )

        movements = [

            self._build_response(item)

            for item in result["items"]

        ]

        return {

            "items": movements,

            "total": result["total"],

            "page": page,

            "limit": limit,

            "total_pages": (

                result["total"] + limit - 1
            ) // limit

        }