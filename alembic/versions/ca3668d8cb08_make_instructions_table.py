"""make_instructions_table

Revision ID: ca3668d8cb08
Revises: 
Create Date: 2023-05-17 11:00:05.062886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3668d8cb08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'instructions',
        sa.Column('instruction_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.recipe_id')),
        sa.Column('step_order', sa.Integer),
        sa.Column('step_name', sa.String),
    )


def downgrade():
    op.drop_table('instructions')
