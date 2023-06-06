"""Add unique constraint to instructions

Revision ID: a9e9fc1c554a
Revises: 75016b62cdd8
Create Date: 2023-06-04 19:27:01.397099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e9fc1c554a'
down_revision = '75016b62cdd8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_recipe_step_order", "instructions", ["recipe_id", "step_order"])

def downgrade() -> None:
    op.drop_constraint("uq_recipe_step_order", "instructions", type_="unique")

