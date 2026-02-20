"""Backfill tenant_id to default tenant

Revision ID: 009
Revises: 008
Create Date: 2026-02-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Default tenant id is 1 (created in 007)
    default_id = 1
    op.execute(sa.text("UPDATE users SET tenant_id = :id WHERE tenant_id IS NULL").bindparams(id=default_id))
    op.execute(sa.text("UPDATE contacts SET tenant_id = :id WHERE tenant_id IS NULL").bindparams(id=default_id))
    op.execute(sa.text("UPDATE companies SET tenant_id = :id WHERE tenant_id IS NULL").bindparams(id=default_id))
    op.execute(sa.text("UPDATE notes SET tenant_id = :id WHERE tenant_id IS NULL").bindparams(id=default_id))
    op.execute(sa.text("UPDATE activities SET tenant_id = :id WHERE tenant_id IS NULL").bindparams(id=default_id))
    op.execute(sa.text("UPDATE audit_logs SET tenant_id = :id WHERE tenant_id IS NULL").bindparams(id=default_id))


def downgrade() -> None:
    op.execute(sa.text("UPDATE users SET tenant_id = NULL"))
    op.execute(sa.text("UPDATE contacts SET tenant_id = NULL"))
    op.execute(sa.text("UPDATE companies SET tenant_id = NULL"))
    op.execute(sa.text("UPDATE notes SET tenant_id = NULL"))
    op.execute(sa.text("UPDATE activities SET tenant_id = NULL"))
    op.execute(sa.text("UPDATE audit_logs SET tenant_id = NULL"))
