"""add content column to  posts table

Revision ID: 09c88b1c091e
Revises: ddbf6e5950f8
Create Date: 2022-11-20 16:36:44.304342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c88b1c091e'
down_revision = 'ddbf6e5950f8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
