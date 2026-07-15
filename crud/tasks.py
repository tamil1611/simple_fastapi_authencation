from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import schemas
from app.models import Task


def create_task(
    db: Session,
    task_data: schemas.TaskCreate,
    user_id: int,
) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status.value,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(
    db: Session,
    user_id: int,
    status_filter: schemas.TaskStatus | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Task]:
    query = db.query(Task).filter(Task.user_id == user_id)

    if status_filter is not None:
        query = query.filter(Task.status == status_filter.value)

    if search:
        search_text = search.strip()
        if search_text:
            pattern = f"%{search_text}%"
            query = query.filter(
                or_(
                    Task.title.ilike(pattern),
                    Task.description.ilike(pattern),
                )
            )

    return query.order_by(Task.id.desc()).offset(skip).limit(limit).all()


def get_task_by_id(
    db: Session,
    task_id: int,
) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(
    db: Session,
    task: Task,
    task_data: schemas.TaskUpdate,
) -> Task:
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status.value

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
) -> None:
    db.delete(task)
    db.commit()