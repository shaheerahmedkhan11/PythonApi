"""create notes table

Revision ID: 93a95b9a71fd
Revises:
Create Date: 2026-01-03 14:39:45.612278

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "93a95b9a71fd"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title",sa.String(),nullable=False),
        sa.Column("content",sa.String(),nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("notes")
    """Downgrade schema."""
    pass
