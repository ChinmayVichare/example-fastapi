"""add user table

Revision ID: 5187c503257c
Revises: ad0540db16d7
Create Date: 2021-11-17 19:09:05.088614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5187c503257c'
down_revision = 'ad0540db16d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
