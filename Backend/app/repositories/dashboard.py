# from datetime import  date

# from app.models.appointment import AppointmentStatus
# from app.models.doctor import DoctorStatus
# from app.models.patient import PatientStatus


# class DashboardRepository:

#     def __init__(self, db):
#         self.db = db

#     # ==========================
#     # Hospital
#     # ==========================

#     async def get_hospital(
#         self,
#         hospital_id: str
#     ):

#         return await self.db.hospitals.find_one(
#             {
#                 "hospital_id": hospital_id
#             }
#         )

#     # ==========================
#     # Patients
#     # ==========================

#     async def get_total_patients(
#         self,
#         hospital_id: str
#     ):

#         return await self.db.patients.count_documents(
#             {
#                 "hospital_id": hospital_id
#             }
#         )

#     async def get_active_patients(
#         self,
#         hospital_id: str
#     ):

#         return await self.db.patients.count_documents(
#             {
#                 "hospital_id": hospital_id,
#                 "status": PatientStatus.ACTIVE
#             }
#         )

#     # ==========================
#     # Doctors
#     # ==========================

#     async def get_total_doctors(
#         self,
#         hospital_id: str
#     ):

#         return await self.db.doctors.count_documents(
#             {
#                 "hospital_id": hospital_id
#             }
#         )

#     async def get_active_doctors(
#         self,
#         hospital_id: str
#     ):

#         return await self.db.doctors.count_documents(
#             {
#                 "hospital_id": hospital_id,
#                 "status": DoctorStatus.ACTIVE
#             }
#         )

#     # ==========================
#     # Departments
#     # ==========================

#     async def get_total_departments(
#         self,
#         hospital_id: str
#     ):

#         return await self.db.departments.count_documents(
#             {
#                 "hospital_id": hospital_id
#             }
#         )

#     # ==========================
#     # Today's Appointments
#     # ==========================

#     async def get_today_appointments(
#         self,
#         hospital_id: str,
#         today: date
#     ):

#         return await self.db.appointments.count_documents(
#             {
#                 "hospital_id": hospital_id,
#                 "appointment_date": today
#             }
#         )

#     async def get_today_completed(
#         self,
#         hospital_id: str,
#         today: date
#     ):

#         return await self.db.appointments.count_documents(
#             {
#                 "hospital_id": hospital_id,
#                 "appointment_date": today.isoformat(),
#                 "status": AppointmentStatus.COMPLETED
#             }
#         )

#     async def get_today_cancelled(
#         self,
#         hospital_id: str,
#         today: date
#     ):
#         return await self.db.appointments.count_documents(
#             {
#                 "hospital_id": hospital_id,
#                 "appointment_date": today.isoformat(),  # Result: "2026-07-22"
#                 "status": AppointmentStatus.CANCELLED
#             }
#         )

#     # ==========================
#     # Appointment Status Summary
#     # ==========================

#     async def get_status_summary(
#         self,
#         hospital_id: str,
#         today: date
#     ):

#         pipeline = [

#             {
#                 "$match": {
#                     "hospital_id": hospital_id,
#                     "appointment_date": today
#                 }
#             },

#             {
#                 "$group": {
#                     "_id": "$status",
#                     "count": {
#                         "$sum": 1
#                     }
#                 }
#             }

#         ]

#         return await self.db.appointments.aggregate(
#             pipeline
#         ).to_list(length=None)


#     # ==========================
#     # Recent Appointments
#     # ==========================

#     async def get_recent_appointments(
#         self,
#         hospital_id: str,
#         limit: int = 10
#     ):

#         cursor = self.db.appointments.find(
#             {
#                 "hospital_id": hospital_id,
#                 "status": {
#                     "$nin": [
#                         AppointmentStatus.CANCELLED,
#                         AppointmentStatus.NO_SHOW
#                     ]
#                 }
#             }
#         ).sort(
#             [
#                 ("appointment_date", -1),
#                 ("appointment_time", -1)
#             ]
#         ).limit(limit)

#         return await cursor.to_list(length=limit)
  


from datetime import datetime, date, time

from app.models.appointment import AppointmentStatus
from app.models.doctor import DoctorStatus
from app.models.patient import PatientStatus


class DashboardRepository:

    def __init__(self, db):
        self.db = db

    # ==========================
    # Hospital
    # ==========================

    async def get_hospital(
        self,
        hospital_id: str
    ):

        return await self.db.hospitals.find_one(
            {
                "hospital_id": hospital_id
            }
        )

    # ==========================
    # Patients
    # ==========================

    async def get_total_patients(
        self,
        hospital_id: str
    ):

        return await self.db.patients.count_documents(
            {
                "hospital_id": hospital_id
            }
        )

    async def get_active_patients(
        self,
        hospital_id: str
    ):

        return await self.db.patients.count_documents(
            {
                "hospital_id": hospital_id,
                "status": PatientStatus.ACTIVE
            }
        )

    # ==========================
    # Doctors
    # ==========================

    async def get_total_doctors(
        self,
        hospital_id: str
    ):

        return await self.db.doctors.count_documents(
            {
                "hospital_id": hospital_id
            }
        )

    async def get_active_doctors(
        self,
        hospital_id: str
    ):

        return await self.db.doctors.count_documents(
            {
                "hospital_id": hospital_id,
                "status": DoctorStatus.ACTIVE
            }
        )

    # ==========================
    # Departments
    # ==========================

    async def get_total_departments(
        self,
        hospital_id: str
    ):

        return await self.db.departments.count_documents(
            {
                "hospital_id": hospital_id
            }
        )

    # ==========================
    # Today's Appointments
    # ==========================

    async def get_today_appointments(
        self,
        hospital_id: str,
        today: date
    ):
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        return await self.db.appointments.count_documents(
            {
                "hospital_id": hospital_id,
                "appointment_date": {
                    "$gte": start_of_day,
                    "$lte": end_of_day
                }
            }
        )

    async def get_today_completed(
        self,
        hospital_id: str,
        today: date
    ):
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        return await self.db.appointments.count_documents(
            {
                "hospital_id": hospital_id,
                "appointment_date": {
                    "$gte": start_of_day,
                    "$lte": end_of_day
                },
                "status": AppointmentStatus.COMPLETED
            }
        )

    async def get_today_cancelled(
        self,
        hospital_id: str,
        today: date
    ):
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        return await self.db.appointments.count_documents(
            {
                "hospital_id": hospital_id,
                "appointment_date": {
                    "$gte": start_of_day,
                    "$lte": end_of_day
                },
                "status": AppointmentStatus.CANCELLED
            }
        )

    # ==========================
    # Appointment Status Summary
    # ==========================

    async def get_status_summary(
        self,
        hospital_id: str,
        today: date
    ):
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        pipeline = [
            {
                "$match": {
                    "hospital_id": hospital_id,
                    "appointment_date": {
                        "$gte": start_of_day,
                        "$lte": end_of_day
                    }
                }
            },
            {
                "$group": {
                    "_id": "$status",
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]

        return await self.db.appointments.aggregate(
            pipeline
        ).to_list(length=None)

    # ==========================
    # Recent Appointments
    # ==========================

    async def get_recent_appointments(
        self,
        hospital_id: str,
        limit: int = 10
    ):

        cursor = self.db.appointments.find(
            {
                "hospital_id": hospital_id,
                "status": {
                    "$nin": [
                        AppointmentStatus.CANCELLED,
                        AppointmentStatus.NO_SHOW
                    ]
                }
            }
        ).sort(
            [
                ("appointment_date", -1),
                ("appointment_time", -1)
            ]
        ).limit(limit)

        return await cursor.to_list(length=limit)