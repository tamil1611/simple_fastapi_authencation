from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

engine_options: dict[str, object] = {}

if settings.database_url.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

    if settings.database_url == "sqlite:///:memory:":
        engine_options["poolclass"] = StaticPool

engine = create_engine(settings.database_url, **engine_options)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(
    dbapi_connection,
    _connection_record,
) -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()