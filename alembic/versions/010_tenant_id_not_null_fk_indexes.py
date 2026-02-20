"""Set tenant_id NOT NULL, FK to tenants, indexes

Revision ID: 010
Revises: 009
Create Date: 2026-02-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLES = ("users", "contacts", "companies", "notes", "activities", "audit_logs")


def upgrade() -> None:
    for table in TABLES:
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.alter_column(
                "tenant_id",
                existing_type=sa.Integer(),
                nullable=False,
            )
            batch_op.create_foreign_key(
                op.f(f"fk_{table}_tenant_id_tenants"),
                "tenants",
                ["tenant_id"],
                ["id"],
            )
            batch_op.create_index(op.f(f"ix_{table}_tenant_id"), ["tenant_id"], unique=False)


def downgrade() -> None:
    for table in TABLES:
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.drop_index(op.f(f"ix_{table}_tenant_id"), table_name=table)
            batch_op.drop_constraint(op.f(f"fk_{table}_tenant_id_tenants"), type_="foreignkey")
            batch_op.alter_column(
                "tenant_id",
                existing_type=sa.Integer(),
                nullable=True,
            )
