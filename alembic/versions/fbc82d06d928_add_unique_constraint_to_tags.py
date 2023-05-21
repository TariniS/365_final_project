"""add_unique_constraint_to_tags

Revision ID: fbc82d06d928
Revises: 6265a379810c
Create Date: 2023-05-19 14:34:31.637649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc82d06d928'
down_revision = '6265a379810c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_tags_name', 'tags', ['tag'])

def downgrade() -> None:
    op.drop_constraint('uq_tags_name', 'tags', type_='unique')
