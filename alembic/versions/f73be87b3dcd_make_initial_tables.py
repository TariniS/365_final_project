"""make_initial_tables

Revision ID: f73be87b3dcd
Revises: 
Create Date: 2023-05-17 16:56:39.398586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f73be87b3dcd'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('firstname', sa.String(length=100), nullable=False),
        sa.Column('lastname', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=100), nullable=False),
    ),
    op.create_table(
        'ingredients',
        sa.Column('ingredient_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('core_ingredient', sa.String(length=255), nullable=False)
    ),
    op.create_table(
        'recipes',
        sa.Column('recipe_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_name', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('total_time', sa.Text),
        sa.Column('servings', sa.Integer),
        sa.Column('spice_level', sa.Integer),
        sa.Column('cooking_level', sa.Integer),
    ),
    op.create_table(
        'recipe_ratings',
        sa.Column('rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('recipe_rating', sa.Integer),
        sa.Column('recipe_comment', sa.String),
        sa.Column('time_stamp', sa.Date),
    ),
    op.create_table(
        'instructions',
        sa.Column('instruction_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id')),
        sa.Column('step_order', sa.Integer),
        sa.Column('step_name', sa.String),
    ),
    op.create_table(
        'recipe_tags',
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.tag_id'), primary_key=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id'), primary_key=True),
        sa.Column('tag', sa.Text),
    ),
    op.create_table(
        'tags',
        sa.Column('tag_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('tag', sa.Text),
    ),
    op.create_table(
        'recipe_ingredients',
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id'), primary_key=True),
        sa.Column('ingredient_id', sa.Integer, sa.ForeignKey('ingredients.ingredient_id'), primary_key=True),
        sa.Column('quantity', sa.Float),
        sa.Column('measurement', sa.String),
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('recipe_ingredients')
    op.drop_table('recipe_tags')
    op.drop_table('instructions')
    op.drop_table('recipe_ratings')
    op.drop_table('recipes')
    op.drop_table('ingredients')


