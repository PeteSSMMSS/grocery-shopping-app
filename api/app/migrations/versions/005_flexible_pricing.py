"""add flexible pricing system

Revision ID: 005
Revises: 004
Create Date: 2025-10-29 13:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to products
    op.add_column('products', sa.Column('price_type', sa.String(20), nullable=False, server_default='per_package'))
    op.add_column('products', sa.Column('package_size', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('package_unit', sa.String(10), nullable=True))
    
    # Migrate existing data: package_size_grams -> package_size with unit 'g'
    op.execute("""
        UPDATE products 
        SET 
            package_size = package_size_grams,
            package_unit = 'g',
            price_type = 'per_package'
        WHERE package_size_grams IS NOT NULL
    """)
    
    # Drop old column from products
    op.drop_column('products', 'package_size_grams')
    
    # Update meal_ingredients table
    op.add_column('meal_ingredients', sa.Column('quantity', sa.Float(), nullable=True))
    op.add_column('meal_ingredients', sa.Column('quantity_unit', sa.String(10), nullable=False, server_default='g'))
    
    # Migrate meal ingredients data
    op.execute("""
        UPDATE meal_ingredients 
        SET quantity = quantity_grams
        WHERE quantity_grams IS NOT NULL
    """)
    
    # Drop old column from meal_ingredients
    op.drop_column('meal_ingredients', 'quantity_grams')
    
    # Make quantity NOT NULL after migration
    op.alter_column('meal_ingredients', 'quantity', nullable=False)


def downgrade() -> None:
    # Revert meal_ingredients
    op.add_column('meal_ingredients', sa.Column('quantity_grams', sa.Integer(), nullable=True))
    op.execute("""
        UPDATE meal_ingredients 
        SET quantity_grams = CAST(quantity AS INTEGER)
        WHERE quantity_unit = 'g'
    """)
    op.drop_column('meal_ingredients', 'quantity_unit')
    op.drop_column('meal_ingredients', 'quantity')
    
    # Revert products
    op.add_column('products', sa.Column('package_size_grams', sa.Integer(), nullable=True))
    op.execute("""
        UPDATE products 
        SET package_size_grams = CAST(package_size AS INTEGER)
        WHERE package_unit = 'g' AND package_size IS NOT NULL
    """)
    op.drop_column('products', 'package_unit')
    op.drop_column('products', 'package_size')
    op.drop_column('products', 'price_type')
