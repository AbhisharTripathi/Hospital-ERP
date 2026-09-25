from fastapi import HTTPException, status
from app.models.supplier import SupplierModel
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate
)
from app.repositories.supplier import SupplierRepository
from app.repositories.counters import CountersRepository
from app.utils.id_generator import IDGenerator
from app.schemas.pagination import build_pagination_meta

class SupplierService:
    def __init__(
        self,
        supplier_repository: SupplierRepository,
        counter_repository: CountersRepository
    ):
        self.supplier_repo = supplier_repository
        self.counter_repo = counter_repository

    # --------------------------------------------------
    # Response Builder
    # --------------------------------------------------

    def _build_response(
        self,
        supplier: dict
    ):
        return SupplierResponse(
            supplier_id=supplier["supplier_id"],
            hospital_id=supplier["hospital_id"],
            supplier_name=supplier["supplier_name"],
            contact_person=supplier.get("contact_person"),
            phone=supplier.get("phone"),
            email=supplier.get("email"),
            address=supplier.get("address"),
            gst_number=supplier.get("gst_number"),
            is_active=supplier["is_active"],
            created_at=supplier["created_at"],
            updated_at=supplier["updated_at"]
        )

    # --------------------------------------------------
    # Create Supplier
    # --------------------------------------------------

    async def create_supplier(
        self,
        current_user,
        supplier_data: SupplierCreate
    ):
        hospital_id = current_user["hospital_id"]

        # ---------------- Duplicate Validation ----------------

        existing = await self.supplier_repo.find_duplicate(
            hospital_id=hospital_id,
            supplier_name=supplier_data.supplier_name,
            gst_number=supplier_data.gst_number
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Supplier already exists"
            )

        supplier_id = await IDGenerator.generate_supplier_id(
            self.counter_repo
        )

        # ---------------- Model ----------------

        supplier_model = SupplierModel(
            supplier_id=supplier_id,
            hospital_id=hospital_id,
            supplier_name=supplier_data.supplier_name,
            contact_person=supplier_data.contact_person,
            phone=supplier_data.phone,
            email=supplier_data.email,
            address=supplier_data.address,
            gst_number=supplier_data.gst_number,
            is_active=True,
            created_by=current_user["user_id"]
        )

        # -----------Create----------

        await self.supplier_repo.create_supplier(
            supplier_model.model_dump(mode="json")
        )

        # -----------Response-----------

        return self._build_response(
            supplier_model.model_dump(mode="json")
        )

    # -----Search/Autocomplete--------

    async def search_suppliers(
        self,
        current_user,
        search: str,
        limit: int = 10
    ):
        hospital_id = current_user["hospital_id"]
        search = search.strip()

        if not search or len(search) < 2:
            return []

        suppliers = await self.supplier_repo.search_suppliers(
            hospital_id=hospital_id,
            search=search,
            limit=limit
        )

        return [
            self._build_response(item)
            for item in suppliers
        ]

    # --------Get all Suppliers------------

    async def get_all_suppliers(
        self,
        current_user,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        is_active: bool | None = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):
        result = await self.supplier_repo.get_all_suppliers(
            hospital_id=current_user["hospital_id"],
            page=page,
            limit=limit,
            search=search,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )

        suppliers = [
            self._build_response(item)
            for item in result.get("items", [])
        ]

        pagination = build_pagination_meta(
            page=page,
            limit=limit,
            total_records=result["total"]
        )

        return {
            "data": suppliers,
            "pagination": pagination
        }

    # ----------Get supplier By id-------------

    async def get_supplier_by_id(
        self,
        current_user,
        supplier_id: str
    ):
        supplier = await self.supplier_repo.get_by_supplier_id(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id
        )

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )

        return self._build_response(supplier)

    # -------Update Supplier-----------

    async def update_supplier(
        self,
        current_user,
        supplier_id: str,
        supplier_data: SupplierUpdate
    ):
        supplier = await self.supplier_repo.get_by_supplier_id(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id
        )
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier Not found"
            )

        # -------Update Data----------------

        update_data = supplier_data.model_dump(
            exclude_unset=True,
            mode="json"
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nothing to update"
            )

        # -------------Update--------------

        await self.supplier_repo.update_supplier(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id,
            update_data=update_data
        )

        # --------Get Updated Supplier-----------

        updated = await self.supplier_repo.get_by_supplier_id(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id
        )
        
        return self._build_response(updated)

    # ----------- Update Supplier Status--------

    async def update_status(
        self,
        current_user,
        supplier_id: str,
        is_active: bool
    ):
        supplier = await self.supplier_repo.get_by_supplier_id(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id
        )

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier Not found"
            )

        if supplier["is_active"] == is_active:
            state = "active" if is_active else "inactive"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Supplier is already {state}"
            )

        # -----------Update Status----------

        await self.supplier_repo.update_status(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id,
            is_active=is_active
        )

        # -------------Get Updated Supplier---------------

        # FIXED: Variable passed correctly as 'supplier_id' instead of 'self.supplier_repo'
        updated = await self.supplier_repo.get_by_supplier_id(
            hospital_id=current_user["hospital_id"],
            supplier_id=supplier_id
        )
        return self._build_response(updated)

    async def delete_supplier(self, current_user: dict, supplier_id: str):
        hospital_id = current_user.get("hospital_id")
        
        # 1. Supplier exist karta hai ya nahi check karein
        existing_supplier = await self.supplier_repo.get_by_supplier_id(
            hospital_id=hospital_id, 
            supplier_id=supplier_id
        )
        if not existing_supplier:
            raise HTTPException(
                status_code=404, 
                detail="Supplier not found"
            )

        # 2. Repository ke delete_supplier ko call karein
        result = await self.supplier_repo.delete_supplier(
            hospital_id=hospital_id, 
            supplier_id=supplier_id
        )
        
        return {"message": "Supplier deleted successfully"}