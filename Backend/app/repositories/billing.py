from datetime import datetime, timezone

from app.models.billing import PaymentStatus

from bson import ObjectId
class BillingRepository:

    def __init__(self, db):
        self.db = db

    def serialize_mongo_doc(self,doc: dict) -> dict:
            if not doc:
                return doc
            # Convert _id and any other ObjectId to string
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
            return doc

    # ==========================
    # Create
    # ==========================

    async def create_bill(
        self,
        bill_data: dict
    ):

        result = await self.db.billings.insert_one(
            bill_data
        )

        return result.inserted_id

    # ==========================
    # Get By Bill ID
    # ==========================

    async def get_bill_by_id(
        self,
        hospital_id: str,
        bill_id: str
    ):

        bill= await self.db.billings.find_one(

            {
                "hospital_id": hospital_id,
                "bill_id": bill_id
            }

        )
        return self.serialize_mongo_doc(bill)

    # ==========================
    # Get By Invoice Number
    # ==========================

    async def get_by_invoice_number(
        self,
        hospital_id: str,
        invoice_number: str
    ):

        return await self.db.billings.find_one(

            {
                "hospital_id": hospital_id,
                "invoice_number": invoice_number
            }

        )

    # ==========================
    # Get All Bills
    # ==========================
    
    async def get_all_bills(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        patient_id: str | None = None,

        doctor_id: str | None = None,

        payment_status: PaymentStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        query = {

            "hospital_id": hospital_id

        }

        if patient_id:
            query["patient_id"] = patient_id

        if doctor_id:
            query["doctor_id"] = doctor_id

        if payment_status:
            query["payment_status"] = payment_status

        if search:

            query["$or"] = [

                {
                    "bill_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "invoice_number": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "patient_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "doctor_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.billings.count_documents(
            query
        )

        skip = (page - 1) * limit

        bills = await self.db.billings.find(
            query
        ).sort(
            sort_by,
            sort_order
        ).skip(
            skip
        ).limit(
            limit
        ).to_list(
            length=limit
        )
        serialized_bills = [self.serialize_mongo_doc(bill) for bill in bills]
        return {

            "items": serialized_bills,

            "total": total

        }

    # ==========================
    # Update Bill
    # ==========================

    async def update_bill(

        self,

        hospital_id: str,

        bill_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        return await self.db.billings.update_one(

            {

                "hospital_id": hospital_id,

                "bill_id": bill_id

            },

            {

                "$set": update_data

            }

        )

    # ==========================
    # Update Payment Status
    # ==========================

    async def update_payment_status(

        self,

        hospital_id: str,

        bill_id: str,

        payment_status: PaymentStatus

    ):

        return await self.db.billings.update_one(

            {

                "hospital_id": hospital_id,

                "bill_id": bill_id

            },

            {

                "$set": {

                    "payment_status": payment_status.value,

                    "updated_at": datetime.now(
                        timezone.utc
                    )

                }

            }

        )

    # ==========================
    # Delete
    # ==========================

    async def delete_bill(

        self,

        hospital_id: str,

        bill_id: str

    ):

        return await self.db.billings.delete_one(

            {

                "hospital_id": hospital_id,

                "bill_id": bill_id

            }

        )