"""add index for stock

Revision ID: 5303e5ca6b1b
Revises: 3432124870f8
Create Date: 2016-06-15 09:32:28.461026

"""

# revision identifiers, used by Alembic.
revision = '5303e5ca6b1b'
down_revision = '3432124870f8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('stock_index', 'stocks', ['exchange','symbol'], unique=True)
    pass


def downgrade():
    op.drop_index('stock_index')
    pass
