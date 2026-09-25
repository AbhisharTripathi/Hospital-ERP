from fastapi import (
    HTTPException,
    status
)

from app.models.purchase import (
    PurchaseModel,
    PurchaseStatus
)

from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseUpdate,
    PurchaseResponse
)

from app.repositories.purchase import (
    PurchaseRepository
)

from app.repositories.supplier import (
    SupplierRepository
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
from app.repositories.batch import BatchRepository
from app.repositories.stock import StockRepository
from app.repositories.stock_movement import StockMovementRepository


class PurchaseService:

    def __init__(

        self,

        purchase_repository: PurchaseRepository,

        supplier_repository: SupplierRepository,

        medicine_repository: MedicineRepository,

        counter_repository: CountersRepository,
        batch_repository: BatchRepository,
        stock_repository: StockRepository,
        stock_movement_repository: StockMovementRepository

    ):

        self.purchase_repo = purchase_repository

        self.supplier_repo = supplier_repository

        self.medicine_repo = medicine_repository

        self.counter_repo = counter_repository

        self.batch_repo = batch_repository
        self.stock_repo = stock_repository
        self.stock_movement_repo = stock_movement_repository

    # --------------------------------------------------
    # Response Builder
    # --------------------------------------------------

    def _build_response(
        self,
        purchase: dict
    ):

        return PurchaseResponse(

            purchase_id=purchase["purchase_id"],

            hospital_id=purchase["hospital_id"],

            supplier_id=purchase["supplier_id"],

            invoice_number=purchase["invoice_number"],

            invoice_date=purchase["invoice_date"],

            items=purchase["items"],

            subtotal=purchase["subtotal"],

            discount=purchase["discount"],

            tax=purchase["tax"],

            total_amount=purchase["total_amount"],

            status=purchase["status"],

            created_by=purchase["created_by"],

            created_at=purchase["created_at"],

            updated_at=purchase["updated_at"]

        )

    # --------------------------------------------------
    # Create Purchase
    # --------------------------------------------------

    async def create_purchase(

        self,

        current_user,

        purchase_data: PurchaseCreate

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Supplier Validation ----------------

        supplier = await self.supplier_repo.get_by_supplier_id(

            hospital_id=hospital_id,

            supplier_id=purchase_data.supplier_id

        )

        if not supplier:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Supplier not found"

            )

        # ---------------- Supplier Active ----------------

        if not supplier["is_active"]:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Supplier is inactive"

            )

        # ---------------- Duplicate Invoice ----------------

        existing = await self.purchase_repo.get_by_invoice_number(

            hospital_id=hospital_id,

            invoice_number=purchase_data.invoice_number

        )

        if existing:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Purchase with this invoice number already exists"

            )

        # ---------------- Medicine Validation ----------------

        for item in purchase_data.items:

            medicine = await self.medicine_repo.get_by_medicine_id(

                hospital_id=hospital_id,

                medicine_id=item.medicine_id

            )

            if not medicine:

                raise HTTPException(

                    status_code=status.HTTP_404_NOT_FOUND,

                    detail=(
                        f"Medicine not found: "
                        f"{item.medicine_id}"
                    )

                )

            # ---------------- Medicine Active ----------------

            if not medicine["is_active"]:

                raise HTTPException(

                    status_code=status.HTTP_400_BAD_REQUEST,

                    detail=(
                        f"Medicine is inactive: "
                        f"{item.medicine_id}"
                    )

                )

        # ---------------- Purchase ID ----------------

        purchase_id = await IDGenerator.generate_purchase_id(

            self.counter_repo

        )

        # ---------------- Model ----------------

        purchase_model = PurchaseModel(

            purchase_id=purchase_id,

            hospital_id=hospital_id,

            supplier_id=purchase_data.supplier_id,

            invoice_number=purchase_data.invoice_number,

            invoice_date=purchase_data.invoice_date,

            # items=purchase_data.items,
            items=[item.model_dump() for item in purchase_data.items],

            subtotal=purchase_data.subtotal,

            discount=purchase_data.discount,

            tax=purchase_data.tax,

            total_amount=purchase_data.total_amount,

            status=PurchaseStatus.DRAFT,

            created_by=current_user["user_id"]

        )

        # ---------------- Create ----------------

        await self.purchase_repo.create_purchase(

            purchase_model.model_dump(
                mode="json"
            )

        )

        # ---------------- Response ----------------

        return self._build_response(

            purchase_model.model_dump(
                mode="json"
            )

        )

    

   
     
    

    

    

    # --------------------------------------------------
    # Get Purchase By ID
    # --------------------------------------------------

    
    
    async def get_purchase_by_id(

        self,

        current_user,

        purchase_id: str

    ):

        purchase = await self.purchase_repo.get_by_purchase_id(

            hospital_id=current_user["hospital_id"],

            purchase_id=purchase_id

        )

        if not purchase:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Purchase not found"

            )

        return self._build_response(

            purchase

        )

    # --------------------------------------------------
    # Get Supplier Purchase History
    # --------------------------------------------------

    async def get_supplier_purchases(

        self,

        current_user,

        supplier_id: str

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Supplier Exists ----------------

        supplier = await self.supplier_repo.get_by_supplier_id(

            hospital_id=hospital_id,

            supplier_id=supplier_id

        )

        if not supplier:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Supplier not found"

            )

        purchases = await self.purchase_repo.get_by_supplier(

            hospital_id=hospital_id,

            supplier_id=supplier_id

        )

        return [

            self._build_response(

                purchase

            )

            for purchase in purchases

        ]

    # --------------------------------------------------
    # Get All Purchases
    # --------------------------------------------------

    async def get_all_purchases(

        self,

        current_user,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        supplier_id: str | None = None,

        status: PurchaseStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        result = await self.purchase_repo.get_all_purchases(

            hospital_id=current_user["hospital_id"],

            page=page,

            limit=limit,

            search=search,

            supplier_id=supplier_id,

            status=status,

            sort_by=sort_by,

            sort_order=sort_order

        )

        purchases = [

            self._build_response(

                purchase

            )

            for purchase in result["items"]

        ]

        return {

            "items": purchases,

            "total": result["total"],

            "page": page,

            "limit": limit,

            "total_pages": (

                result["total"] + limit - 1
            ) // limit

        }

    # --------------------------------------------------
    # Update Purchase
    # --------------------------------------------------

    async def update_purchase(

        self,

        current_user,

        purchase_id: str,

        purchase_data: PurchaseUpdate

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Purchase Exists ----------------

        purchase = await self.purchase_repo.get_by_purchase_id(

            hospital_id=hospital_id,

            purchase_id=purchase_id

        )

        if not purchase:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Purchase not found"

            )

        # ---------------- Update Data ----------------

        update_data = purchase_data.model_dump(

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

        await self.purchase_repo.update_purchase(

            hospital_id=hospital_id,

            purchase_id=purchase_id,

            update_data=update_data

        )

        # ---------------- Get Updated Purchase ----------------

        updated = await self.purchase_repo.get_by_purchase_id(

            hospital_id=hospital_id,

            purchase_id=purchase_id

        )

        return self._build_response(

            updated

        )

    # --------------------------------------------------
    # Update Purchase Status
    # --------------------------------------------------

    async def update_status(

        self,

        current_user,

        purchase_id: str,

        purchase_status: PurchaseStatus

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Purchase Exists ----------------

        purchase = await self.purchase_repo.get_by_purchase_id(

            hospital_id=hospital_id,

            purchase_id=purchase_id

        )

        if not purchase:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Purchase not found"

            )

        # ---------------- Same Status ----------------

        if purchase["status"] == purchase_status.value:

            state = purchase_status.value.lower()

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail=f"Purchase is already {state}"

            )

        # ---------------- Update Status ----------------

        await self.purchase_repo.update_status(

            hospital_id=hospital_id,

            purchase_id=purchase_id,

            status=purchase_status

        )

        # ---------------- Get Updated Purchase ----------------

        updated = await self.purchase_repo.get_by_purchase_id(

            hospital_id=hospital_id,

            purchase_id=purchase_id

        )

        return self._build_response(

            updated

        )



    # --------------------------------------------------
    # Receive Purchase 
    # --------------------------------------------------

    async def receive_purchase(
        self,
        current_user,
        purchase_id: str
    ):
        hospital_id = current_user["hospital_id"]
        user_id = current_user["user_id"]

        # ---------------------------------------------
        # Purchase Exists
        # ---------------------------------------------

        purchase = await self.purchase_repo.get_by_purchase_id(
            hospital_id=hospital_id,
            purchase_id=purchase_id
        )

        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found"
            )

        # ---------------------------------------------
        # Purchase Status Validation
        # ---------------------------------------------

        if purchase["status"] == PurchaseStatus.RECEIVED.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Purchase is already received"
            )

        if purchase["status"] == PurchaseStatus.CANCELLED.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled purchase cannot be received"
            )

        # ---------------------------------------------
        # Process Each Purchase Item
        # ---------------------------------------------

        for item in purchase["items"]:

            medicine_id = item["medicine_id"]
            batch_number = item["batch_number"]
            quantity = item["quantity"]

            # -----------------------------------------
            # Medicine Validation
            # -----------------------------------------

            medicine = await self.medicine_repo.get_by_medicine_id(
                hospital_id=hospital_id,
                medicine_id=medicine_id
            )

            if not medicine:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Medicine not found: {medicine_id}"
                )

            if not medicine["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Medicine is inactive: {medicine_id}"
                )

            # -----------------------------------------
            # Find Existing Batch
            # -----------------------------------------

            batch = await self.batch_repo.find_by_medicine_and_batch(
                hospital_id=hospital_id,
                medicine_id=medicine_id,
                batch_number=batch_number
            )

            # -----------------------------------------
            # Create Batch If Not Exists
            # -----------------------------------------

            if not batch:

                batch_id = await IDGenerator.generate_batch_id(
                    self.counter_repo
                )

                batch_data = {
                    "batch_id": batch_id,
                    "hospital_id": hospital_id,
                    "medicine_id": medicine_id,
                    "batch_number": batch_number,
                    "expiry_date": item["expiry_date"],
                    "purchase_price": item["purchase_price"],
                    "unit": item["unit"],
                    "status": "ACTIVE"
                }

                await self.batch_repo.create_batch(
                    batch_data
                )

                batch = batch_data

            else:

                batch_id = batch["batch_id"]

            # -----------------------------------------
            # Find Existing Stock
            # -----------------------------------------

            stock = await self.stock_repo.get_by_medicine_batch(
                hospital_id=hospital_id,
                medicine_id=medicine_id,
                batch_id=batch_id
            )

            # -----------------------------------------
            # Create Stock If Not Exists
            # -----------------------------------------

            if not stock:

                stock_id = await IDGenerator.generate_stock_id(
                    self.counter_repo
                )

                stock_data = {
                    "stock_id": stock_id,
                    "hospital_id": hospital_id,
                    "medicine_id": medicine_id,
                    "batch_id": batch_id,
                    "quantity": quantity,
                    "reserved_quantity": 0,
                    "available_quantity": quantity,
                    "status": "AVAILABLE"
                }

                await self.stock_repo.create_stock(
                    stock_data
                )

                stock = stock_data

            # -----------------------------------------
            # Increase Existing Stock
            # -----------------------------------------

            else:

                await self.stock_repo.increase_quantity(
                    hospital_id=hospital_id,
                    stock_id=stock["stock_id"],
                    quantity=quantity
                )

            # -----------------------------------------
            # Create Stock Movement IN
            # -----------------------------------------

            movement_id = await IDGenerator.generate_stock_movement_id(
                self.counter_repo
            )

            movement_data = {
                "movement_id": movement_id,
                "hospital_id": hospital_id,
                "stock_id": stock["stock_id"],
                "medicine_id": medicine_id,
                "batch_id": batch_id,
                "movement_type": "IN",
                "quantity": quantity,
                "reference_type": "PURCHASE",
                "reference_id": purchase_id,
                "reason": "Purchase received",
                "created_by": user_id
            }

            await self.stock_movement_repo.create_movement(
                movement_data
            )

        # ---------------------------------------------
        # Update Purchase Status
        # ---------------------------------------------

        await self.purchase_repo.update_status(
            hospital_id=hospital_id,
            purchase_id=purchase_id,
            status=PurchaseStatus.RECEIVED
        )

        # ---------------------------------------------
        # Get Updated Purchase
        # ---------------------------------------------

        updated = await self.purchase_repo.get_by_purchase_id(
            hospital_id=hospital_id,
            purchase_id=purchase_id
        )

        return self._build_response(updated)



    # --------------------------------------------------
    # Delete Purchase
    # --------------------------------------------------

    async def delete_purchase(

        self,

        current_user,

        purchase_id: str

    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Purchase Exists ----------------

        purchase = await self.purchase_repo.get_by_purchase_id(

            hospital_id=hospital_id,

            purchase_id=purchase_id

        )

        if not purchase:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Purchase not found"

            )

        # ---------------- Received Purchase ----------------

        if purchase["status"] == PurchaseStatus.RECEIVED.value:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Received purchase cannot be deleted"

            )



        

        # ---------------- Delete ----------------

        await self.purchase_repo.delete_purchase(

            hospital_id=hospital_id,

            purchase_id=purchase_id

        )

        return {

            "success": True,

            "message": "Purchase deleted successfully"

        }