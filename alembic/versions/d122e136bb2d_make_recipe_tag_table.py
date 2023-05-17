"""make_recipe_tag_table

Revision ID: d122e136bb2d
Revises: 46689a335688
Create Date: 2023-05-17 11:01:08.700439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd122e136bb2d'
down_revision = '46689a335688'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recipe_tags',
        sa.Column('tag_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id')),
        sa.Column('tag', sa.Text),
    )


def downgrade():
    op.drop_table('recipe_tags')
