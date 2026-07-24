from datetime import datetime, timezone



class DepartmentRepository:

    def __init__(self, db):
        self.db = db

    async def create_department(
        self,
        department_data: dict
    ):

        result = await self.db.departments.insert_one(
            department_data
        )

        return result.inserted_id

    async def create_many_departments(
        self,
        departments: list[dict]
    ):

        if not departments:
            return None

        result = await self.db.departments.insert_many(
            departments
        )

        return result.inserted_ids

    async def get_by_name(
        self,
        hospital_id: str,
        name: str
    ):

        return await self.db.departments.find_one(
            {
                "hospital_id": hospital_id,
                "name": name
            }
        )

    async def get_by_code(
        self,
        hospital_id: str,
        code: str
    ):

        return await self.db.departments.find_one(
            {
                "hospital_id": hospital_id,
                "code": code
            }
        )

    async def get_by_department_id(
        self,
        department_id: str,
        hospital_id: str
    ):

        return await self.db.departments.find_one(
            {
                "department_id": department_id,
                "hospital_id": hospital_id
            }
        )

    async def get_all_departments(
        self,
        hospital_id: str,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        is_active: bool | None = None,
        sort_by: str = "name",
        sort_order: int = 1
    ):
        query = {
            "hospital_id": hospital_id
        }

        if is_active is not None:
            query["is_active"] = is_active

        if search:
            query["$or"] = [

                {
                    "name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "code": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.departments.count_documents(query)
        skip = (page - 1) * limit
        departments = await self.db.departments.find(
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
            "items": departments,
            "total": total
        }
        
        # cursor = self.db.departments.find(
        #     {
        #         "hospital_id": hospital_id
        #     }
        # )

        # return await cursor.to_list(length=None)

    async def update_department(
        self,
        department_id: str,
        hospital_id: str,
        update_data: dict
    ):

        return await self.db.departments.update_one(
            {
                "department_id": department_id,
                "hospital_id": hospital_id
            },
            {
                "$set": update_data
            }
        )

    async def update_status(
        self,
        department_id: str,
        hospital_id: str,
        is_active: bool
    ):

        return await self.db.departments.update_one(
            {
                "department_id": department_id,
                "hospital_id": hospital_id
            },
            {
                "$set": {
                    "is_active": is_active,
                    "updated_at": datetime.now(
                        timezone.utc
                    )
                }
            }
        )