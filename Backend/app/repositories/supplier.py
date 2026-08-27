from datetime import datetime, timezone
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


# ==========================================
# Serialize Mongo Document
# ==========================================

def serialize_mongo_doc(doc: dict):
    if not doc:
        return doc

    cleaned = {}

    for key, value in doc.items():
        if isinstance(value, ObjectId):
            cleaned[key] = str(value)
        elif isinstance(value, dict):
            cleaned[key] = serialize_mongo_doc(value)
        elif isinstance(value, list):
            cleaned[key] = [
                serialize_mongo_doc(item)
                if isinstance(item, dict)
                else (
                    str(item)
                    if isinstance(item, ObjectId)
                    else item
                )
                for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned


# ==========================================
# Repository
# ==========================================

class SupplierRepository:
    def __init__(self, db):
        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_supplier(
        self,
        supplier_data: dict
    ):
        safe_data = jsonable_encoder(supplier_data)
        result = await self.db.suppliers.insert_one(safe_data)
        return result.inserted_id

    # ==========================================
    # Get By Supplier ID (FIXED TYPO: hosital_id -> hospital_id)
    # ==========================================

    async def get_by_supplier_id(
        self,
        hospital_id: str,
        supplier_id: str
    ):
        supplier = await self.db.suppliers.find_one({
            "hospital_id": hospital_id,  # FIX: Corrected spelling here
            "supplier_id": supplier_id
        })

        return serialize_mongo_doc(supplier)

    # ==========================================
    # Check Duplicate Supplier
    # ==========================================

    async def find_duplicate(
        self,
        hospital_id: str,
        supplier_name: str,
        gst_number: str | None
    ):
        query = {
            "hospital_id": hospital_id,
            "supplier_name": supplier_name
        }

        if gst_number:
            query["gst_number"] = gst_number

        supplier = await self.db.suppliers.find_one(query)
        return serialize_mongo_doc(supplier)

    # ==========================================
    # Search / Autocomplete
    # ==========================================

    async def search_suppliers(
        self,
        hospital_id: str,
        search: str,
        limit: int = 10
    ):
        query = {
            "hospital_id": hospital_id,
            "is_active": True,
            "$or": [
                {
                    "supplier_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "contact_person": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "phone": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]
        }

        suppliers = await self.db.suppliers.find(query).sort(
            "supplier_name", 1
        ).limit(limit).to_list(length=limit)

        return [serialize_mongo_doc(item) for item in suppliers]

    # ==========================================
    # Get All (FIXED TYPO: $optins -> $options)
    # ==========================================

    async def get_all_suppliers(
        self,
        hospital_id: str,
        page: int,
        limit: int,
        search: str | None,
        is_active: bool | None,
        sort_by: str,
        sort_order: int
    ):
        query = {
            "hospital_id": hospital_id
        }

        if search:
            query["$or"] = [
                {
                    "supplier_name": {
                        "$regex": search,
                        "$options": "i"  # FIX: Corrected spelling here
                    }
                },
                {
                    "contact_person": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "phone": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "gst_number": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]

        if is_active is not None:
            query["is_active"] = is_active

        total = await self.db.suppliers.count_documents(query)
        skip = (page - 1) * limit

        suppliers = await self.db.suppliers.find(query).sort(
            sort_by, sort_order
        ).skip(skip).limit(limit).to_list(length=limit)

        return {
            "items": [serialize_mongo_doc(item) for item in suppliers],
            "total": total
        }

    # ==========================================
    # Update
    # ==========================================

    async def update_supplier(
        self,
        hospital_id: str,
        supplier_id: str,
        update_data: dict
    ):
        update_data["updated_at"] = datetime.now(timezone.utc)
        safe_data = jsonable_encoder(update_data)

        return await self.db.suppliers.update_one(
            {
                "hospital_id": hospital_id,
                "supplier_id": supplier_id
            },
            {
                "$set": safe_data
            }
        )

    # ==========================================
    # Update Active Status
    # ==========================================

    async def update_status(
        self,
        hospital_id: str,
        supplier_id: str,
        is_active: bool
    ):
        return await self.db.suppliers.update_one(
            {
                "hospital_id": hospital_id,
                "supplier_id": supplier_id
            },
            {
                "$set": {
                    "is_active": is_active,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

    # ==========================================
    # Delete (FIXED TYPE HINT: StopIteration -> str)
    # ==========================================

    async def delete_supplier(
        self,
        hospital_id: str,
        supplier_id: str  # FIX: Corrected type hint
    ):
        return await self.db.suppliers.delete_one({
            "hospital_id": hospital_id,
            "supplier_id": supplier_id
        })