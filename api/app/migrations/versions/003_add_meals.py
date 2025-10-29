"""add meals and meal_ingredients tables

Revision ID: 003
Revises: 002
Create Date: 2025-10-29 12:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create meals table
    op.create_table(
        'meals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('meal_type', sa.String(20), nullable=False),  # breakfast, lunch, dinner
        sa.Column('preparation', sa.Text(), nullable=True),
        sa.Column('total_cost_cents', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meals_id'), 'meals', ['id'], unique=False)
    op.create_index(op.f('ix_meals_name'), 'meals', ['name'], unique=False)
    op.create_index(op.f('ix_meals_meal_type'), 'meals', ['meal_type'], unique=False)

    # Create meal_ingredients table
    op.create_table(
        'meal_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meal_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity_grams', sa.Float(), nullable=False),  # Menge in Gramm
        sa.Column('cost_cents', sa.Integer(), nullable=False),  # Berechnete Kosten
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT')
    )
    op.create_index(op.f('ix_meal_ingredients_id'), 'meal_ingredients', ['id'], unique=False)
    op.create_index(op.f('ix_meal_ingredients_meal_id'), 'meal_ingredients', ['meal_id'], unique=False)
    op.create_index(op.f('ix_meal_ingredients_product_id'), 'meal_ingredients', ['product_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_meal_ingredients_product_id'), table_name='meal_ingredients')
    op.drop_index(op.f('ix_meal_ingredients_meal_id'), table_name='meal_ingredients')
    op.drop_index(op.f('ix_meal_ingredients_id'), table_name='meal_ingredients')
    op.drop_table('meal_ingredients')
    
    op.drop_index(op.f('ix_meals_meal_type'), table_name='meals')
    op.drop_index(op.f('ix_meals_name'), table_name='meals')
    op.drop_index(op.f('ix_meals_id'), table_name='meals')
    op.drop_table('meals')
