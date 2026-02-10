"""Contact form and validation schema."""

import re

from pydantic import BaseModel, Field, field_validator


def _email_regex() -> re.Pattern[str]:
    return re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class ContactFormSchema(BaseModel):
    """Schema for create/update form: full_name required, email/phone/company optional; email validated when present."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=64)
    company: str | None = Field(None, max_length=255)

    model_config = {"extra": "forbid"}

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_if_present(cls, v: str | None) -> str | None:
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        s = v.strip()
        if not _email_regex().match(s):
            raise ValueError("Invalid email format")
        return s
