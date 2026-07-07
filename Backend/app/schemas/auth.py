from pydantic import BaseModel, EmailStr,Field


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class UserInfo(BaseModel):
    user_id: str
    email: EmailStr
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user:UserInfo

class SetPasswordRequest(BaseModel):

    token: str

    password: str = Field(
        min_length=6,
        max_length=100
    )