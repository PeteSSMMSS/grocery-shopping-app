"""feat: Add supermarkets and multi-list support

Revision ID: add_supermarkets
Revises: <previous_revision>
Create Date: 2025-10-31 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_supermarkets'
down_revision = None  # Will be set automatically
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create supermarkets table
    op.create_table(
        'supermarkets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_supermarkets_id'), 'supermarkets', ['id'], unique=False)
    op.create_index(op.f('ix_supermarkets_name'), 'supermarkets', ['name'], unique=True)

    # Insert default supermarkets
    op.execute("""
        INSERT INTO supermarkets (name, color) VALUES
        ('Netto', '#FFCC00'),
        ('Lidl', '#0050AA'),
        ('REWE', '#CC071E'),
        ('dm', '#009FE3'),
        ('Aldi', '#0088CC'),
        ('Edeka', '#FFD600'),
        ('Kaufland', '#E30613')
    """)

    # Rename table lists to shopping_lists
    op.rename_table('lists', 'shopping_lists')
    
    # Add supermarket_id to shopping_lists
    op.add_column('shopping_lists', sa.Column('supermarket_id', sa.Integer(), nullable=True))
    op.add_column('shopping_lists', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.create_foreign_key('fk_shopping_lists_supermarket', 'shopping_lists', 'supermarkets', ['supermarket_id'], ['id'])
    op.create_index(op.f('ix_shopping_lists_supermarket_id'), 'shopping_lists', ['supermarket_id'], unique=False)
    
    # Set default supermarket (Netto) for existing lists
    op.execute("UPDATE shopping_lists SET supermarket_id = (SELECT id FROM supermarkets WHERE name = 'Netto' LIMIT 1) WHERE supermarket_id IS NULL")
    
    # Make supermarket_id required
    op.alter_column('shopping_lists', 'supermarket_id', nullable=False)
    
    # Add supermarket_id to products
    op.add_column('products', sa.Column('supermarket_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_products_supermarket', 'products', 'supermarkets', ['supermarket_id'], ['id'])
    op.create_index(op.f('ix_products_supermarket_id'), 'products', ['supermarket_id'], unique=False)
    
    # Set default supermarket (Netto) for existing products
    op.execute("UPDATE products SET supermarket_id = (SELECT id FROM supermarkets WHERE name = 'Netto' LIMIT 1) WHERE supermarket_id IS NULL")
    
    # Make supermarket_id required
    op.alter_column('products', 'supermarket_id', nullable=False)
    
    # Update foreign key in list_items
    op.drop_constraint('list_items_list_id_fkey', 'list_items', type_='foreignkey')
    op.create_foreign_key('fk_list_items_shopping_list', 'list_items', 'shopping_lists', ['list_id'], ['id'])
    
    # Update foreign key in purchases
    op.drop_constraint('purchases_list_id_fkey', 'purchases', type_='foreignkey')
    op.create_foreign_key('fk_purchases_shopping_list', 'purchases', 'shopping_lists', ['list_id'], ['id'])


def downgrade() -> None:
    # Reverse foreign keys
    op.drop_constraint('fk_purchases_shopping_list', 'purchases', type_='foreignkey')
    op.create_foreign_key('purchases_list_id_fkey', 'purchases', 'lists', ['list_id'], ['id'])
    
    op.drop_constraint('fk_list_items_shopping_list', 'list_items', type_='foreignkey')
    op.create_foreign_key('list_items_list_id_fkey', 'list_items', 'lists', ['list_id'], ['id'])
    
    # Remove supermarket_id from products
    op.drop_index(op.f('ix_products_supermarket_id'), table_name='products')
    op.drop_constraint('fk_products_supermarket', 'products', type_='foreignkey')
    op.drop_column('products', 'supermarket_id')
    
    # Remove supermarket_id from shopping_lists
    op.drop_index(op.f('ix_shopping_lists_supermarket_id'), table_name='shopping_lists')
    op.drop_constraint('fk_shopping_lists_supermarket', 'shopping_lists', type_='foreignkey')
    op.drop_column('shopping_lists', 'supermarket_id')
    op.drop_column('shopping_lists', 'created_at')
    
    # Rename table back
    op.rename_table('shopping_lists', 'lists')
    
    # Drop supermarkets table
    op.drop_index(op.f('ix_supermarkets_name'), table_name='supermarkets')
    op.drop_index(op.f('ix_supermarkets_id'), table_name='supermarkets')
    op.drop_table('supermarkets')
