from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole
    name: str = Field(min_length=2, max_length=255)
    phone: str = Field(min_length=8, max_length=20)
    language: str = Field(default="en", max_length=32)
    # pyre-ignore[6]
    age: int | None = Field(default=None, ge=0, le=120)
    blood_type: str | None = Field(default=None, max_length=8)
    allergies: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)
    recent_diagnoses: list[str] = Field(default_factory=list)
    consent_granted: bool = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    role: UserRole
    swasthya_id: str | None
    name: str
    language: str
    age: int | None
    blood_type: str | None
    allergies: list[str]
    current_medications: list[str]
    recent_diagnoses: list[str]
    consent_granted: bool
    created_at: datetime


class SendOTPRequest(BaseModel):
    phone: str = Field(..., examples=["9876543210"])


class VerifyOTPRequest(BaseModel):
    phone: str = Field(..., examples=["9876543210"])
    otp: str = Field(..., examples=["123456"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
