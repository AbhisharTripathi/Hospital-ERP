import bcrypt #password keep safe
 
import jwt # userr gets login through jwt token

from datetime import datetime, timedelta, timezone
from app.core.config import settings


def hash_password(
        password: str
) -> str:

    return bcrypt.hashpw(
        password.encode("utf-8"), # password ko pahle byte me badalte hai
        bcrypt.gensalt() #ye ek random string daal deta hai agar do logo ke password same bhi ho to bhi hash value different ho
    ).decode("utf-8")


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict) -> str:
    

    payload = data.copy() # payload me user ki information hoti hai

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expire

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token


def decode_token(token: str) -> dict:
    

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )