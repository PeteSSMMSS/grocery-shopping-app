"""refactor unit_weight to package_size_grams

Revision ID: 004
Revises: 003
Create Date: 2025-10-29 12:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new column
    op.add_column('products', sa.Column('package_size_grams', sa.Integer(), nullable=True))
    
    # Optional: Migrate existing data (parse unit_weight strings)
    # This is a best-effort migration - manual cleanup may be needed
    op.execute("""
        UPDATE products 
        SET package_size_grams = CASE
            WHEN unit_weight ~ '^[0-9]+g$' THEN CAST(REGEXP_REPLACE(unit_weight, '[^0-9]', '', 'g') AS INTEGER)
            WHEN unit_weight ~ '^[0-9.]+kg$' THEN CAST(REGEXP_REPLACE(unit_weight, '[^0-9.]', '', 'g') AS FLOAT) * 1000
            WHEN unit_weight ~ '^[0-9]+\s*g$' THEN CAST(REGEXP_REPLACE(unit_weight, '[^0-9]', '', 'g') AS INTEGER)
            ELSE NULL
        END
        WHERE unit_weight IS NOT NULL
    """)
    
    # Drop old column
    op.drop_column('products', 'unit_weight')


def downgrade() -> None:
    # Add back old column
    op.add_column('products', sa.Column('unit_weight', sa.String(50), nullable=True))
    
    # Migrate data back (convert grams to string)
    op.execute("""
        UPDATE products 
        SET unit_weight = CASE
            WHEN package_size_grams >= 1000 THEN (package_size_grams / 1000)::TEXT || 'kg'
            ELSE package_size_grams::TEXT || 'g'
        END
        WHERE package_size_grams IS NOT NULL
    """)
    
    # Drop new column
    op.drop_column('products', 'package_size_grams')
