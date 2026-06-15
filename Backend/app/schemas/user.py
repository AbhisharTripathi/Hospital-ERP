from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserCreate(BaseModel):

    username: str

    email: EmailStr

    password: str

    role: UserRole


class UserResponse(BaseModel):

    user_id: str

    username: str

    email: EmailStr

    role: UserRole

    is_active: bool