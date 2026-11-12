
"""Add Category

Revision ID: 7cb0c59197fe
Revises: 7ec9bc7b9565
Create Date: 2026-11-12 20:55:45.070489

"""
from alembic import op
import sqlalchemy as sa


revision = '7cb0c59197fe'
down_revision = '7ec9bc7b9565'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('category_id', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            'fk_products_category_id_categories',
            'categories',
            ['category_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_products_category_id_categories',
            type_='foreignkey'
        )
        batch_op.drop_column('category_id')

    op.drop_table('categories')
