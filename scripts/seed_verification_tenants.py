"""Create tenants A and B and one admin user per tenant for multi-tenant verification.

Run after migrations and before verification (e.g. pytest or manual curl/Python).
Uses APP_ENV and DATABASE_URL from environment. Idempotent: skips if tenants already exist.

Usage (from project root):
  python -c "from scripts.seed_verification_tenants import run; run()"
  # or
  uv run python -m scripts.seed_verification_tenants
"""

from __future__ import annotations

import sys
from pathlib import Path

# Project root on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select

from app.core.password import hash_password
from app.db.session import get_db_context
from app.models import Tenant, User
from app.models.user import UserRole


TENANT_A_NAME = "Tenant A"
TENANT_B_NAME = "Tenant B"
USER_A_EMAIL = "admin_tenant_a@test.local"
USER_B_EMAIL = "admin_tenant_b@test.local"
VERIFICATION_PASSWORD = "test"


def run() -> None:
    with get_db_context() as db:
        a = db.execute(select(Tenant).where(Tenant.name == TENANT_A_NAME).limit(1)).scalars().first()
        if a is not None:
            print("Tenants A/B already exist; skipping.")
            return

        tenant_a = Tenant(name=TENANT_A_NAME)
        tenant_b = Tenant(name=TENANT_B_NAME)
        db.add(tenant_a)
        db.add(tenant_b)
        db.flush()

        user_a = User(
            tenant_id=tenant_a.id,
            email=USER_A_EMAIL,
            password_hash=hash_password(VERIFICATION_PASSWORD),
            role=UserRole.admin.value,
        )
        user_b = User(
            tenant_id=tenant_b.id,
            email=USER_B_EMAIL,
            password_hash=hash_password(VERIFICATION_PASSWORD),
            role=UserRole.admin.value,
        )
        db.add(user_a)
        db.add(user_b)
        db.flush()
        print(
            f"Created tenants: {TENANT_A_NAME} (id={tenant_a.id}), {TENANT_B_NAME} (id={tenant_b.id}). "
            f"Users: {USER_A_EMAIL}, {USER_B_EMAIL} (password: {VERIFICATION_PASSWORD})"
        )


if __name__ == "__main__":
    run()
