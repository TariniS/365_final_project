"""make_ingredient_tag_table

Revision ID: 46689a335688
Revises: 33c6945c3be0
Create Date: 2023-05-17 11:00:58.885063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46689a335688'
down_revision = '33c6945c3be0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ingredients_tags',
        sa.Column('tag_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('ingredient_id', sa.Integer, sa.ForeignKey('ingredients.ingredient_id')),
        sa.Column('tag', sa.String),
    )


def downgrade():
    op.drop_table('ingredients_tags')