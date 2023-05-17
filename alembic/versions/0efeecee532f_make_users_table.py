"""make_users_table

Revision ID: 0efeecee532f
Revises: ca3668d8cb08
Create Date: 2023-05-17 11:00:14.282369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0efeecee532f'
down_revision = 'ca3668d8cb08'
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
    )


def downgrade():
    op.drop_table('users')
