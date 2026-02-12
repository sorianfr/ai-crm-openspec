"""Company form and validation schema."""

from pydantic import BaseModel, Field, field_validator


class CompanyFormSchema(BaseModel):
    """Schema for create/update company form submissions."""

    name: str = Field(..., min_length=1, max_length=255)

    model_config = {"extra": "forbid"}

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        text = (v or "").strip()
        if not text:
            raise ValueError("Company name is required")
        return text
