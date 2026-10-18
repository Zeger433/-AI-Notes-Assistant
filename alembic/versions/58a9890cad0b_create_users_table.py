"""Create users table

Revision ID: 58a9890cad0b
Revises: e442220daa3e
Create Date: 2026-07-23 08:32:43.071742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58a9890cad0b'
down_revision: Union[str, Sequence[str], None] = 'e442220daa3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
