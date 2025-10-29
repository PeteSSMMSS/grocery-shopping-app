"""Add shopping_events table

Revision ID: 006
Revises: 005
Create Date: 2025-10-29 15:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create shopping_events table
    op.create_table(
        'shopping_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('event_date', sa.Date(), nullable=False),
        sa.Column('total_price_cents', sa.Integer(), nullable=False),
        sa.Column('items', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_shopping_events_event_date', 'shopping_events', ['event_date'])


def downgrade() -> None:
    op.drop_index('ix_shopping_events_event_date')
    op.drop_table('shopping_events')
