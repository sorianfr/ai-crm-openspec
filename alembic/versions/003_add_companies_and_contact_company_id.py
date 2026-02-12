"""Add companies table and optional contact.company_id

Revision ID: 003
Revises: 8b27dbf72065
Create Date: 2026-02-12

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "003"
down_revision: Union[str, None] = "8b27dbf72065"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "companies" not in inspector.get_table_names():
        op.create_table(
            "companies",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    inspector = sa.inspect(bind)
    contact_columns = {column["name"] for column in inspector.get_columns("contacts")}
    if "company_id" not in contact_columns:
        with op.batch_alter_table("contacts", schema=None) as batch_op:
            batch_op.add_column(sa.Column("company_id", sa.Integer(), nullable=True))

    inspector = sa.inspect(bind)
    index_names = {index["name"] for index in inspector.get_indexes("contacts")}
    has_company_fk = any(
        fk.get("referred_table") == "companies"
        and fk.get("constrained_columns") == ["company_id"]
        for fk in inspector.get_foreign_keys("contacts")
    )
    needs_index = "ix_contacts_company_id" not in index_names
    needs_fk = not has_company_fk

    if needs_index or needs_fk:
        with op.batch_alter_table("contacts", schema=None) as batch_op:
            if needs_index:
                batch_op.create_index("ix_contacts_company_id", ["company_id"], unique=False)
            if needs_fk:
                batch_op.create_foreign_key(
                    "fk_contacts_company_id_companies",
                    "companies",
                    ["company_id"],
                    ["id"],
                    ondelete="SET NULL",
                )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "contacts" in inspector.get_table_names():
        contact_columns = {column["name"] for column in inspector.get_columns("contacts")}
        index_names = {index["name"] for index in inspector.get_indexes("contacts")}
        if "company_id" in contact_columns:
            with op.batch_alter_table("contacts", schema=None) as batch_op:
                if "ix_contacts_company_id" in index_names:
                    batch_op.drop_index("ix_contacts_company_id")
                batch_op.drop_column("company_id")

    inspector = sa.inspect(bind)
    if "companies" in inspector.get_table_names():
        op.drop_table("companies")
