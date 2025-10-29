"""add unit_weight to products

Revision ID: 002
Revises: 001
Create Date: 2025-10-29 11:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add unit_weight column to products table
    op.add_column('products', sa.Column('unit_weight', sa.String(50), nullable=True))


def downgrade() -> None:
    # Remove unit_weight column from products table
    op.drop_column('products', 'unit_weight')
