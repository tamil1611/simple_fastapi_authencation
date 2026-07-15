from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.users import create_user, get_user_by_email
from app.db.session import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def signup(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> User:
    existing_user = get_user_by_email(
        db=db,
        email=str(user_data.email),
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    try:
        return create_user(db=db, user_data=user_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login and generate JWT access token",
)
def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db),
) -> dict[str, str | int]:
    user = get_user_by_email(db=db, email=str(login_data.email))

    if user is None or not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
    }


@router.get(
    "/me",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get logged-in user details",
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user