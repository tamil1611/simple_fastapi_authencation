from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt
from fastapi.security import HTTPBearer

from app.core.config import settings

bearer_scheme = HTTPBearer(
    scheme_name="JWT Bearer Authentication",
    description="Enter the JWT access token received from /auth/login",
    auto_error=False,
)


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError("Password must not exceed 72 bytes")

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int) -> str:
    current_time = datetime.now(timezone.utc)
    expiration_time = current_time + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "iat": current_time,
        "exp": expiration_time,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )