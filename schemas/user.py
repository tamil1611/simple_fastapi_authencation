from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class UserCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        examples=["Manikandaprabu S"],
    )
    email: EmailStr = Field(..., examples=["manikanda@example.com"])
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["StrongPassword@123"],
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        cleaned_value = value.strip()

        if len(cleaned_value) < 2:
            raise ValueError(
                "Full name must contain at least 2 characters"
            )

        return cleaned_value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 bytes")

        return value


class UserLogin(BaseModel):
    email: EmailStr = Field(..., examples=["manikanda@example.com"])
    password: str = Field(
        ...,
        min_length=1,
        examples=["StrongPassword@123"],
    )


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)