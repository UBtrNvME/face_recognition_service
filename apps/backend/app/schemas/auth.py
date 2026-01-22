# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None


# LoginRequest removed - using FastAPI's OAuth2PasswordRequestForm instead


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str | None = Field(None, max_length=255)

