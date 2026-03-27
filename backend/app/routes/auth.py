from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_roles
from app.core.security import create_access_token
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, SendOTPRequest, VerifyOTPRequest, TokenResponse, UserPublic
from app.services.user_service import authenticate_user, create_user, get_user_by_email, get_user_by_phone
from app.services.otp_service import otp_service
from database.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/send-otp")
async def send_otp(payload: SendOTPRequest, db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user_by_phone(db, payload.phone)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    otp = await otp_service.create_otp(payload.phone)
    # The actual SMS dispatch would happen in otp_service.create_otp
    return {"message": "OTP sent successfully", "DEBUG_OTP": otp}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(payload: VerifyOTPRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await get_user_by_phone(db, payload.phone)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    is_valid = await otp_service.verify_otp(payload.phone, payload.otp)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP")
        
    token = create_access_token(subject=user.id, role=user.role.value)
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = await create_user(db, payload)
    token = create_access_token(subject=user.id, role=user.role.value)
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.id, role=user.role.value)
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)


@router.get("/admin-only")
async def admin_only(current_admin: User = Depends(require_roles(UserRole.admin))) -> dict:
    return {"message": f"Welcome Admin {current_admin.name}"}
