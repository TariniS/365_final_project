"""make_recipe_rating_table

Revision ID: 33c6945c3be0
Revises: f8c18539c6ee
Create Date: 2023-05-17 11:00:45.904093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33c6945c3be0'
down_revision = 'f8c18539c6ee'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recipe_ratings',
        sa.Column('rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id')),
        sa.Column('recipe_rating', sa.Integer),
        sa.Column('recipe_comment', sa.String),
        sa.Column('time_stamp', sa.Date),
    )


def downgrade():
    op.drop_table('recipe_ratings')
