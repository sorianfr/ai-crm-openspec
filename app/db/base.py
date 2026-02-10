"""Database base configuration and metadata for Alembic."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models. Import this for new models."""

    pass
