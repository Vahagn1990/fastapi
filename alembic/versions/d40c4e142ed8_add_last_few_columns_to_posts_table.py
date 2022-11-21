"""add last few columns to posts table

Revision ID: d40c4e142ed8
Revises: c6b1e7c69b9d
Create Date: 2022-11-20 17:02:05.486536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd40c4e142ed8'
down_revision = 'c6b1e7c69b9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published',sa.Boolean(),nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
    ))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
