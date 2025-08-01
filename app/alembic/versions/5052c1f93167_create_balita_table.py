"""create balita table

Revision ID: 5052c1f93167
Revises: 
Create Date: 2025-07-21 13:00:17.665197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5052c1f93167'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posyandu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_posyandu', sa.String(), nullable=False),
    sa.Column('alamat', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posyandu_id'), 'posyandu', ['id'], unique=False)
    op.create_table('balita',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(), nullable=False),
    sa.Column('nik', sa.String(length=16), nullable=False),
    sa.Column('nama_orang_tua', sa.String(), nullable=False),
    sa.Column('posyandu_id', sa.Integer(), nullable=True),
    sa.Column('tanggal_lahir', sa.DateTime(), nullable=True),
    sa.Column('jenis_kelamin', sa.String(length=1), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['posyandu_id'], ['posyandu.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nik')
    )
    op.create_index(op.f('ix_balita_id'), 'balita', ['id'], unique=False)
    op.create_table('pemeriksaan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('balita_id', sa.Integer(), nullable=True),
    sa.Column('tanggal_pemeriksaan', sa.DateTime(), nullable=True),
    sa.Column('usia_bulan', sa.Integer(), nullable=True),
    sa.Column('tinggi_badan', sa.DECIMAL(precision=5, scale=2), nullable=True),
    sa.Column('berat_badan', sa.DECIMAL(precision=5, scale=2), nullable=True),
    sa.Column('status_stunting', sa.Enum('NORMAL', 'STUNTING', name='statusstunting'), nullable=True),
    sa.Column('total_pemeriksaan', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['balita_id'], ['balita.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pemeriksaan_id'), 'pemeriksaan', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pemeriksaan_id'), table_name='pemeriksaan')
    op.drop_table('pemeriksaan')
    op.drop_index(op.f('ix_balita_id'), table_name='balita')
    op.drop_table('balita')
    op.drop_index(op.f('ix_posyandu_id'), table_name='posyandu')
    op.drop_table('posyandu')
    # ### end Alembic commands ###
