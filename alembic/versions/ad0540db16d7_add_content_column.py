"""add content column

Revision ID: ad0540db16d7
Revises: 9480f86c9511
Create Date: 2021-11-17 19:00:55.001203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad0540db16d7'
down_revision = '9480f86c9511'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
