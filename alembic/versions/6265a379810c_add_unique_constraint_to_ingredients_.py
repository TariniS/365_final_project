"""Add unique constraint to ingredients.name

Revision ID: 6265a379810c
Revises: f73be87b3dcd
Create Date: 2023-05-18 14:57:46.668400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6265a379810c'
down_revision = 'f73be87b3dcd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_ingredients_name', 'ingredients', ['name'])

def downgrade() -> None:
    op.drop_constraint('uq_ingredients_name', 'ingredients', type_='unique')

