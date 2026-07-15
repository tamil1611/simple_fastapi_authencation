import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


def _get_positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default))

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a valid integer") from exc

    if value <= 0:
        raise RuntimeError(f"{name} must be greater than zero")

    return value


@lru_cache
def get_settings() -> Settings:
    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY is missing. Add SECRET_KEY to the .env file."
        )

    return Settings(
        app_name=os.getenv("APP_NAME", "FastAPI Task Manager API"),
        environment=os.getenv("ENVIRONMENT", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./task_manager.db"),
        secret_key=secret_key,
        algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_expire_minutes=_get_positive_int(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            30,
        ),
    )


settings = get_settings()