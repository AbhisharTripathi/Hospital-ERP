from app.models.patient import PatientStatus


class PatientRepository:

    def __init__(self, db):
        self.db = db

    async def create_patient(
        self,
        patient_data
    ):
        result = await self.db.patients.insert_one(
            patient_data
        )
        return result.inserted_id

    async def get_all_patients(
        self,
        hospital_id: str,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        status: PatientStatus | None = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):

        query = {
            "hospital_id": hospital_id
        }

        if status:
            query["status"] = status

        if search:

            query["$or"] = [

                {
                    "patient_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "first_name": {
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
                    "address": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.patients.count_documents(
            query
        )

        skip = (page - 1) * limit

        patients = await self.db.patients.find(
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

        return {

            "items": patients,

            "total": total

        }

    async def get_patient_by_id(
        self,
        hospital_id: str,
        patient_id: str
    ):

        return await self.db.patients.find_one(

            {   "hospital_id": hospital_id,
                "patient_id": patient_id
            }

        )

    async def get_by_phone(
        self,
        hospital_id: str,
        phone: str
    ):

        return await self.db.patients.find_one(

            {  "hospital_id": hospital_id,
                "phone": phone
            }

        )

    async def search_patients(
        self,
        filters,
        limit: int = 20
    ):

        return await self.db.patients.find(
            filters
        ).to_list(
            length=limit
        )

    async def update_by_patient_id(
        self,
        patient_id,
        hospital_id: str,
        updated_data
    ):

        return await self.db.patients.update_one(

            {   "hospital_id": hospital_id,
                "patient_id": patient_id
            },

            {
                "$set": updated_data
            }

        )

    async def delete_by_patient_id(
        self,
        hospital_id: str,
        patient_id
    ):

        return await self.db.patients.delete_one(

            {   "hospital_id": hospital_id,
                "patient_id": patient_id
            }

        )

    async def delete_all_patients(
        self
    ):

        return await self.db.patients.delete_many({})