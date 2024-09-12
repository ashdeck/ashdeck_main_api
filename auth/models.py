from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class Login(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    access_token: str
    refresh_token: str


class SignUp(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
    created_at: datetime = datetime.now(timezone.utc)


class SignUpResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
