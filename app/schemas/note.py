"""Note form and validation schema."""

from pydantic import BaseModel, Field, field_validator


class NoteFormSchema(BaseModel):
    """Schema for add-note form: content required, non-empty after strip."""

    content: str = Field(..., min_length=1, max_length=65535)

    model_config = {"extra": "forbid"}

    @field_validator("content", mode="before")
    @classmethod
    def strip_and_validate_non_empty(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Content must be a string")
        s = v.strip()
        if not s:
            raise ValueError("Content is required")
        return s
