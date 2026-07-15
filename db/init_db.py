from datetime import datetime, timezone

from sqlalchemy import inspect, text

from app import models as _models
from app.db.base import Base
from app.db.session import engine


def _archive_legacy_tasks_table() -> None:
    inspector = inspect(engine)

    if "tasks" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("tasks")}

    if "user_id" in columns:
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    legacy_table_name = f"tasks_legacy_{timestamp}"

    with engine.begin() as connection:
        connection.execute(
            text(f'ALTER TABLE tasks RENAME TO "{legacy_table_name}"')
        )


def init_db() -> None:
    _ = _models
    _archive_legacy_tasks_table()
    Base.metadata.create_all(bind=engine)