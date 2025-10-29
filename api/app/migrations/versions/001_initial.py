"""Initial migration - create all tables

Revision ID: 001
Revises: 
Create Date: 2025-10-29

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=True)

    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_is_active'), 'products', ['is_active'], unique=False)
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)

    # Create product_prices table
    op.create_table(
        'product_prices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('price_cents', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('valid_from', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_prices_id'), 'product_prices', ['id'], unique=False)
    op.create_index(op.f('ix_product_prices_product_id'), 'product_prices', ['product_id'], unique=False)

    # Create lists table
    op.create_table(
        'lists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lists_id'), 'lists', ['id'], unique=False)
    op.create_index(op.f('ix_lists_is_active'), 'lists', ['is_active'], unique=False)

    # Create list_items table
    op.create_table(
        'list_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('list_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('is_checked', sa.Boolean(), nullable=True),
        sa.Column('added_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_list_items_id'), 'list_items', ['id'], unique=False)
    op.create_index(op.f('ix_list_items_list_id'), 'list_items', ['list_id'], unique=False)
    op.create_index(op.f('ix_list_items_product_id'), 'list_items', ['product_id'], unique=False)

    # Create purchases table
    op.create_table(
        'purchases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('list_id', sa.Integer(), nullable=False),
        sa.Column('purchased_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('total_cents', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchases_id'), 'purchases', ['id'], unique=False)
    op.create_index(op.f('ix_purchases_list_id'), 'purchases', ['list_id'], unique=False)

    # Create purchase_items table
    op.create_table(
        'purchase_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('purchase_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('price_cents_at_purchase', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_items_id'), 'purchase_items', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_items_product_id'), 'purchase_items', ['product_id'], unique=False)
    op.create_index(op.f('ix_purchase_items_purchase_id'), 'purchase_items', ['purchase_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_purchase_items_purchase_id'), table_name='purchase_items')
    op.drop_index(op.f('ix_purchase_items_product_id'), table_name='purchase_items')
    op.drop_index(op.f('ix_purchase_items_id'), table_name='purchase_items')
    op.drop_table('purchase_items')
    
    op.drop_index(op.f('ix_purchases_list_id'), table_name='purchases')
    op.drop_index(op.f('ix_purchases_id'), table_name='purchases')
    op.drop_table('purchases')
    
    op.drop_index(op.f('ix_list_items_product_id'), table_name='list_items')
    op.drop_index(op.f('ix_list_items_list_id'), table_name='list_items')
    op.drop_index(op.f('ix_list_items_id'), table_name='list_items')
    op.drop_table('list_items')
    
    op.drop_index(op.f('ix_lists_is_active'), table_name='lists')
    op.drop_index(op.f('ix_lists_id'), table_name='lists')
    op.drop_table('lists')
    
    op.drop_index(op.f('ix_product_prices_product_id'), table_name='product_prices')
    op.drop_index(op.f('ix_product_prices_id'), table_name='product_prices')
    op.drop_table('product_prices')
    
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_index(op.f('ix_products_is_active'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
