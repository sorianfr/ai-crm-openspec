"""Contact model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.company import Company
    from app.models.note import Note


class Contact(Base):
    """Contact entity with legacy company text and optional company reference."""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    company_ref: Mapped["Company | None"] = relationship(
        "Company",
        back_populates="contacts",
    )
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="contact")
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="contact"
    )

    @hybrid_property
    def display_company(self) -> str:
        """Linked company name when present, otherwise legacy company text."""
        if self.company_ref is not None:
            name = getattr(self.company_ref, "name", None)
            if name:
                return name
        return self.company or ""
