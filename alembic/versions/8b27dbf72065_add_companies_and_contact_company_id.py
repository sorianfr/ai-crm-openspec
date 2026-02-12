"""Legacy compatibility revision for companies/contact-company change.

Revision ID: 8b27dbf72065
Revises: 002
Create Date: 2026-02-12

"""

from typing import Sequence, Union


revision: str = "8b27dbf72065"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Compatibility no-op; canonical migration logic is in revision 003."""
    pass


def downgrade() -> None:
    """Compatibility no-op."""
    pass
