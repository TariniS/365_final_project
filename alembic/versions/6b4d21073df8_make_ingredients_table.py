"""make_ingredients_table

Revision ID: 6b4d21073df8
Revises: 0efeecee532f
Create Date: 2023-05-17 11:00:20.071619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b4d21073df8'
down_revision = '0efeecee532f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ingredients',
        sa.Column('ingredient_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('core_ingredient', sa.String(length=255), nullable=False)
    )


def downgrade():
    op.drop_table('ingredients')
