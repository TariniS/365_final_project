"""make_recipe_ingredient_table

Revision ID: f8c18539c6ee
Revises: 7d33977aa1d8
Create Date: 2023-05-17 11:00:39.566766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8c18539c6ee'
down_revision = '7d33977aa1d8'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'recipe_ingredients',
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id'), primary_key=True),
        sa.Column('ingredient_id', sa.Integer, sa.ForeignKey('ingredients.ingredient_id'), primary_key=True),
        sa.Column('quantity', sa.Float),
        sa.Column('measurement', sa.String),
    )


def downgrade():
    op.drop_table('recipe_ingredients')
