"""Optional dev seed: default tenant + one admin user when APP_ENV=development and no users exist."""

from sqlalchemy import select

from app.core.config import APP_ENV
from app.core.password import hash_password
from app.db.session import get_db_context
from app.models import Tenant, User
from app.models.user import UserRole


DEFAULT_TENANT_NAME = "Default"


def seed_dev_admin_if_needed() -> None:
    """If APP_ENV=development and no users exist, ensure default tenant and create one admin. Do not run in production."""
    if APP_ENV != "development":
        return
    with get_db_context() as db:
        existing = db.execute(select(User).limit(1)).scalar_one_or_none()
        if existing is not None:
            return
        default_tenant = db.execute(
            select(Tenant).where(Tenant.name == DEFAULT_TENANT_NAME).limit(1)
        ).scalar_one_or_none()
        if default_tenant is None:
            default_tenant = Tenant(name=DEFAULT_TENANT_NAME)
            db.add(default_tenant)
            db.flush()
        admin = User(
            tenant_id=default_tenant.id,
            email="admin@dev.local",
            password_hash=hash_password("admin"),
            role=UserRole.admin.value,
        )
        db.add(admin)


def seed_dev_admin_if_needed_sync() -> None:
    """Synchronous wrapper for startup event (no async)."""
    seed_dev_admin_if_needed()
