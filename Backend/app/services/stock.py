from fastapi import HTTPException, status

from app.models.stock import (
    StockModel,
    StockStatus
)

from app.schemas.stock import (
    StockCreate,
    StockUpdate,
    StockResponse
)

from app.repositories.stock import (
    StockRepository
)

from app.repositories.medicine import (
    MedicineRepository
)

from app.repositories.batch import (
    BatchRepository
)

from app.repositories.counters import (
    CountersRepository
)

from app.utils.id_generator import (
    IDGenerator
)


class StockService:

    def __init__(
        self,
        stock_repository: StockRepository,
        medicine_repository: MedicineRepository,
        batch_repository: BatchRepository,
        counter_repository: CountersRepository
    ):

        self.stock_repo = stock_repository
        self.medicine_repo = medicine_repository
        self.batch_repo = batch_repository
        self.counter_repo = counter_repository

    # ==========================================
    # Response Builder
    # ==========================================

    def _build_response(
        self,
        stock: dict
    ):

        return StockResponse(

            stock_id=stock["stock_id"],

            hospital_id=stock["hospital_id"],

            medicine_id=stock["medicine_id"],

            batch_id=stock["batch_id"],

            quantity=stock["quantity"],

            reserved_quantity=stock["reserved_quantity"],

            available_quantity=stock["available_quantity"],

            status=stock["status"],

            created_at=stock["created_at"],

            updated_at=stock["updated_at"]

        )

    # ==========================================
    # Create Stock
    # ==========================================

    async def create_stock(
        self,
        current_user,
        stock_data: StockCreate
    ):

        hospital_id = current_user["hospital_id"]

        # --------------------------------------
        # Medicine Validation
        # --------------------------------------

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=hospital_id,

            medicine_id=stock_data.medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        if not medicine["is_active"]:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Medicine is inactive"

            )

        # --------------------------------------
        # Batch Validation
        # --------------------------------------

        batch = await self.batch_repo.get_by_batch_id(

            hospital_id=hospital_id,

            batch_id=stock_data.batch_id

        )

        if not batch:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Batch not found"

            )

        # --------------------------------------
        # Batch-Medicine Validation
        # --------------------------------------

        if batch["medicine_id"] != stock_data.medicine_id:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Batch does not belong to this medicine"

            )

        # --------------------------------------
        # Existing Stock
        # --------------------------------------

        existing = await self.stock_repo.get_by_medicine_batch(

            hospital_id=hospital_id,

            medicine_id=stock_data.medicine_id,

            batch_id=stock_data.batch_id

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Stock already exists for this batch"

            )

        # --------------------------------------
        # Stock ID
        # --------------------------------------

        stock_id = await IDGenerator.generate_stock_id(

            self.counter_repo

        )

        # --------------------------------------
        # Model
        # --------------------------------------

        stock_model = StockModel(

            stock_id=stock_id,

            hospital_id=hospital_id,

            medicine_id=stock_data.medicine_id,

            batch_id=stock_data.batch_id,

            quantity=stock_data.quantity,

            reserved_quantity=0,

            available_quantity=stock_data.quantity,

            status=StockStatus.AVAILABLE,

        )

        # --------------------------------------
        # Create
        # --------------------------------------

        await self.stock_repo.create_stock(

            stock_model.model_dump(
                mode="json"
            )

        )

        # --------------------------------------
        # Response
        # --------------------------------------

        return self._build_response(

            stock_model.model_dump(
                mode="json"
            )

        )

    # ==========================================
    # Get Stock By ID
    # ==========================================

    async def get_stock_by_id(

        self,
        current_user,
        stock_id: str

    ):

        stock = await self.stock_repo.get_by_stock_id(

            hospital_id=current_user["hospital_id"],

            stock_id=stock_id

        )

        if not stock:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Stock not found"

            )

        return self._build_response(
            stock
        )

    # ==========================================
    # Get Medicine Stock
    # ==========================================

    async def get_medicine_stock(

        self,
        current_user,
        medicine_id: str

    ):

        hospital_id = current_user["hospital_id"]

        # --------------------------------------
        # Medicine Validation
        # --------------------------------------

        medicine = await self.medicine_repo.get_by_medicine_id(

            hospital_id=hospital_id,

            medicine_id=medicine_id

        )

        if not medicine:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Medicine not found"

            )

        stocks = await self.stock_repo.get_by_medicine(

            hospital_id=hospital_id,

            medicine_id=medicine_id

        )

        return [

            self._build_response(stock)

            for stock in stocks

        ]

    # ==========================================
    # Get All Stock
    # ==========================================

    async def get_all_stock(

        self,
        current_user,

        page: int = 1,

        limit: int = 20,

        medicine_id: str | None = None,

        batch_id: str | None = None,

        status: StockStatus | None = None,

        sort_by: str = "updated_at",

        sort_order: int = -1

    ):

        result = await self.stock_repo.get_all_stock(

            hospital_id=current_user["hospital_id"],

            page=page,

            limit=limit,

            medicine_id=medicine_id,

            batch_id=batch_id,

            status=status,

            sort_by=sort_by,

            sort_order=sort_order

        )

        stocks = [

            self._build_response(item)

            for item in result["items"]

        ]

        return {

            "items": stocks,

            "total": result["total"],

            "page": page,

            "limit": limit,

            "total_pages": (

                result["total"] + limit - 1
            ) // limit

        }

    # ==========================================
    # Update Stock
    # ==========================================

    async def update_stock(

        self,
        current_user,

        stock_id: str,

        stock_data: StockUpdate

    ):

        hospital_id = current_user["hospital_id"]

        stock = await self.stock_repo.get_by_stock_id(

            hospital_id=hospital_id,

            stock_id=stock_id

        )

        if not stock:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Stock not found"

            )

        update_data = stock_data.model_dump(

            exclude_unset=True,

            mode="json"

        )

        if not update_data:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Nothing to update"

            )

        # --------------------------------------
        # Quantity Validation
        # --------------------------------------

        if "quantity" in update_data:

            quantity = update_data["quantity"]

            reserved_quantity = (

                update_data.get(

                    "reserved_quantity",

                    stock["reserved_quantity"]

                )

            )

            if quantity < reserved_quantity:

                raise HTTPException(

                    status_code=status.HTTP_400_BAD_REQUEST,

                    detail=(
                        "Quantity cannot be less "
                        "than reserved quantity"
                    )

                )

            update_data["available_quantity"] = (

                quantity - reserved_quantity

            )

        # --------------------------------------
        # Reserved Quantity Validation
        # --------------------------------------

        if "reserved_quantity" in update_data:

            reserved_quantity = (

                update_data["reserved_quantity"]

            )

            quantity = (

                update_data.get(

                    "quantity",

                    stock["quantity"]

                )

            )

            if reserved_quantity > quantity:

                raise HTTPException(

                    status_code=status.HTTP_400_BAD_REQUEST,

                    detail=(
                        "Reserved quantity cannot "
                        "exceed total quantity"
                    )

                )

            update_data["available_quantity"] = (

                quantity - reserved_quantity

            )

        # --------------------------------------
        # Update
        # --------------------------------------

        await self.stock_repo.update_stock(

            hospital_id=hospital_id,

            stock_id=stock_id,

            update_data=update_data

        )

        # --------------------------------------
        # Get Updated Stock
        # --------------------------------------

        updated = await self.stock_repo.get_by_stock_id(

            hospital_id=hospital_id,

            stock_id=stock_id

        )

        return self._build_response(
            updated
        )