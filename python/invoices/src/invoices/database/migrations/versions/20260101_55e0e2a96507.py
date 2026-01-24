"""add invoices table

Revision ID: 55e0e2a96507
Revises:
Create Date: 2026-01-01 00:00:00.000000
"""

# fmt: off
# pylint: disable=no-member, line-too-long
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "55e0e2a96507"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade from `null` to `55e0e2a96507`."""
    op.create_table(
        "invoices",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade from `55e0e2a96507` to `null`."""
    op.drop_table("invoices")
