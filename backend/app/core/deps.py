from collections.abc import Callable

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import TokenError, decode_access_token
from app.models.user import User, UserRole
from database.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")


def mock_mode_param(
    mock: bool = Query(
        default=False,
        description="When true, returns deterministic demo-safe mock responses instantly.",
    ),
) -> bool:
    return mock


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exc
    except TokenError:
        raise credentials_exc

    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise credentials_exc
    return user


def require_roles(*allowed_roles: UserRole) -> Callable:
    async def role_dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return role_dependency
