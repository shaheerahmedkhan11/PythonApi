"""add column to notes

Revision ID: 85a6c4c75e6f
Revises: 93a95b9a71fd
Create Date: 2026-01-03 17:42:27.307650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85a6c4c75e6f'
down_revision: Union[str, Sequence[str], None] = '93a95b9a71fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('notes', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('notes', 'created_at')
    pass
