"""Add recipe_type to recipes

Revision ID: 75016b62cdd8
Revises: fbc82d06d928
Create Date: 2023-05-21 12:56:38.359273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75016b62cdd8'
down_revision = 'fbc82d06d928'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('recipes', sa.Column('recipe_type', sa.String))


def downgrade() -> None:
    pass
