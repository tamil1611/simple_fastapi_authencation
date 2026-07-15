from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    pending = "Pending"
    completed = "Completed"


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        examples=["Complete authentication assignment"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Implement JWT authentication using FastAPI"],
    )
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        examples=["Pending"],
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Title cannot be empty")

        return cleaned_value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: TaskStatus | str) -> TaskStatus | str:
        if isinstance(value, TaskStatus):
            return value

        if isinstance(value, str):
            normalized_value = value.strip().lower()

            if normalized_value == "pending":
                return TaskStatus.pending

            if normalized_value == "completed":
                return TaskStatus.completed

        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)