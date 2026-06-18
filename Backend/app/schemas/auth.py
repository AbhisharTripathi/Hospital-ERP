from pydantic import BaseModel, EmailStr


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

  