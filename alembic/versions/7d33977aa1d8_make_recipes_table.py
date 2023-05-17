"""make_recipes_table

Revision ID: 7d33977aa1d8
Revises: 6b4d21073df8
Create Date: 2023-05-17 11:00:26.601074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d33977aa1d8'
down_revision = '6b4d21073df8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recipes',
        sa.Column('recipe_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_name', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('total_time', sa.Text),
        sa.Column('servings', sa.Integer),
        sa.Column('spice_level', sa.Integer),
        sa.Column('cooking_level', sa.Integer),
    )


def downgrade():
    op.drop_table('recipes')
