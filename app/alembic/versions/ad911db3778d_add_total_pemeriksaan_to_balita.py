"""add total_pemeriksaan to balita

Revision ID: ad911db3778d
Revises: 43c09aa24658
Create Date: 2025-07-24 02:58:42.516347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad911db3778d'
down_revision: Union[str, Sequence[str], None] = '43c09aa24658'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
