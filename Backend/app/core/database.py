
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
from app.core.config import settings # iska kaam hai database ka Url(mongo_uri) aur database ka naam laakar dena



client: AsyncIOMotorClient | None = None # database ka rasta hai clint
db: AsyncIOMotorDatabase | None = None # actual database

async def connect_mongo():
    global client, db # inhe globally share kiya jayega
    client = AsyncIOMotorClient(settings.MONGO_URI) 
    db = client[settings.DB_NAME]
    
    
    
    await db.users.create_index(
        [
            ("hospital_id", 1),
            ("email", 1)
        ],
        unique=True     
    )
    await db.users.create_index(
        [
            ("hospital_id", 1),
            ("role", 1)
        ]
   )

    await db.users.create_index(
        [
            ("hospital_id", 1),
            ("status", 1)
        ]
    )
    
    await db.hospitals.create_index(
        "hospital_id",
        unique=True
    )

    await db.hospitals.create_index(
        "slug",
        unique=True
    )

    await db.patients.create_index(
        [
            ("hospital_id", 1),
            ("patient_id", 1)
        ],
        unique=True
    )
    await db.patients.create_index(
        [
            ("hospital_id", 1),
            ("phone", 1)
        ],
        unique=True
    )

    await db.patients.create_index(
        [
            ("hospital_id", 1),
            ("status", 1)
        ]
    )

    
    await db.doctors.create_index(
        [
            ("hospital_id", 1),
            ("doctor_id", 1)
        ],
        unique=True
    )

    await db.doctors.create_index(
        [
            ("hospital_id", 1),
            ("user_id", 1)
        ],
        unique=True
    )

    await db.doctors.create_index(
        [
            ("hospital_id", 1),
            ("license_number", 1)
        ],
        unique=True
    )

    await db.doctors.create_index(
        [
            ("hospital_id", 1),
            ("department_id", 1)
        ]
    )

    await db.doctors.create_index(
        [
            ("hospital_id", 1),
            ("status", 1)
        ]
    )
    
    await db.departments.create_index(
        [
            ("hospital_id", 1),
            ("department_id", 1)
        ],
        unique=True
    )

    await db.departments.create_index(
        [
            ("hospital_id", 1),
            ("name", 1)
        ],
        unique=True
    )

    await db.departments.create_index(
        [
            ("hospital_id", 1),
            ("code", 1)
        ],
        unique=True
    )
    await db.doctor_schedules.create_index(

    [
        ("hospital_id", 1),
        ("schedule_id", 1)
    ],

    unique=True
    )

    await db.doctor_schedules.create_index(

        [
            ("hospital_id", 1),
            ("doctor_id", 1)
        ]

    )

    await db.doctor_schedules.create_index(

        [
            ("hospital_id", 1),
            ("doctor_id", 1),
            ("day_of_week", 1),
            ("is_active", 1)
        ]

    )


print("mongodb is successfully connected and indexs are ready")
    

async def close_mongo():
    global client
    if client:
        client.close()
        print("mongodb connection close securely")


def get_db():
    return db # jab service ya repository ko databsdedd se koi kaam ho to wo db ko get db se hi lega