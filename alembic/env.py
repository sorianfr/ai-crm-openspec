"""Alembic migration environment. Uses app's database URL and metadata."""

import sys
from pathlib import Path

# Ensure project root is on path so `app` can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.core.config import DATABASE_URL
from app.db.base import Base
from app.models import Company, Contact, Note  # noqa: F401 - ensure tables in metadata for autogenerate

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use application's database URL (overrides alembic.ini when set via .env)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (using engine from app)."""
    from app.db.session import engine

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
