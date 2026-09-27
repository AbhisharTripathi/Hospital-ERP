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

class DispenseRepository:

    def __init__(self, db):

        self.db = db


    # ==========================================
    # Create Dispense
    # ==========================================

    async def create_dispense(
        self,
        dispense_data: dict
    ):

        safe_data = jsonable_encoder(
            dispense_data
        )

        result = await self.db.dispenses.insert_one(
            safe_data
        )

        return result.inserted_id


    # ==========================================
    # Get By Dispense ID
    # ==========================================

    async def get_by_dispense_id(
        self,
        hospital_id: str,
        dispense_id: str
    ):

        dispense = await self.db.dispenses.find_one({

            "hospital_id": hospital_id,

            "dispense_id": dispense_id

        })

        return serialize_mongo_doc(
            dispense
        )


    # ==========================================
    # Get By Prescription ID
    # ==========================================

    async def get_by_prescription_id(
        self,
        hospital_id: str,
        prescription_id: str
    ):

        dispense = await self.db.dispenses.find_one({

            "hospital_id": hospital_id,

            "prescription_id": prescription_id

        })

        return serialize_mongo_doc(
            dispense
        )


    # ==========================================
    # Get Patient Dispense History
    # ==========================================

    async def get_by_patient(
        self,
        hospital_id: str,
        patient_id: str
    ):

        cursor = self.db.dispenses.find({

            "hospital_id": hospital_id,

            "patient_id": patient_id

        }).sort(
            "dispensed_at",
            -1
        )

        dispenses = await cursor.to_list(
            length=None
        )

        return [
            serialize_mongo_doc(dispense)
            for dispense in dispenses
        ]