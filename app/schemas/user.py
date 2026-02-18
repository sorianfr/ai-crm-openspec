"""User management request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

ALLOWED_ROLES = ("admin", "manager", "sales")


def _validate_role(v: str) -> str:
    r = (v or "").strip().lower()
    if r not in ALLOWED_ROLES:
        raise ValueError("role must be one of: admin, manager, sales")
    return r


class UserCreate(BaseModel):
    """Body for POST /users."""

    email: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1, max_length=32)

    @field_validator("role")
    @classmethod
    def role_allowed(cls, v: str) -> str:
        return _validate_role(v)


class UserResponse(BaseModel):
    """User payload in API responses (no password/password_hash)."""

    id: int
    email: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserRoleUpdate(BaseModel):
    """Body for PATCH /users/{id}/role."""

    role: str = Field(..., min_length=1, max_length=32)

    @field_validator("role")
    @classmethod
    def role_allowed(cls, v: str) -> str:
        return _validate_role(v)
