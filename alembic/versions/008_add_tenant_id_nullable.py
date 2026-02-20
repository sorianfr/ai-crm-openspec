"""Add tenant_id nullable to all scoped tables

Revision ID: 008
Revises: 007
Create Date: 2026-02-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("tenant_id", sa.Integer(), nullable=True))
    op.add_column("contacts", sa.Column("tenant_id", sa.Integer(), nullable=True))
    op.add_column("companies", sa.Column("tenant_id", sa.Integer(), nullable=True))
    op.add_column("notes", sa.Column("tenant_id", sa.Integer(), nullable=True))
    op.add_column("activities", sa.Column("tenant_id", sa.Integer(), nullable=True))
    op.add_column("audit_logs", sa.Column("tenant_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("audit_logs", "tenant_id")
    op.drop_column("activities", "tenant_id")
    op.drop_column("notes", "tenant_id")
    op.drop_column("companies", "tenant_id")
    op.drop_column("contacts", "tenant_id")
    op.drop_column("users", "tenant_id")
