"""Activity form and validation schema."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


ActivityType = Literal["call", "email", "meeting", "task"]


class ActivityFormSchema(BaseModel):
    """Schema for add-activity form: type, description required, activity_date."""

    type: ActivityType
    description: str = Field(..., min_length=1, max_length=65535)
    activity_date: datetime

    model_config = {"extra": "forbid"}

    @field_validator("description", mode="before")
    @classmethod
    def strip_and_validate_non_empty(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Description must be a string")
        s = v.strip()
        if not s:
            raise ValueError("Description is required")
        return s

    @field_validator("activity_date", mode="before")
    @classmethod
    def parse_activity_date(cls, v: str | datetime) -> datetime:
        if isinstance(v, datetime):
            return v
        if not isinstance(v, str):
            raise ValueError("Activity date must be a string or datetime")
        s = v.strip()
        if not s:
            raise ValueError("Activity date is required")
        for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue
        raise ValueError("Invalid activity date format")
