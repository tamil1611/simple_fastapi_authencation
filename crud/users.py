from sqlalchemy.orm import Session

from app import schemas
from app.core.security import hash_password
from app.models import User


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == normalize_email(email))
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    user_data: schemas.UserCreate,
) -> User:
    user = User(
        full_name=user_data.full_name,
        email=normalize_email(str(user_data.email)),
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user