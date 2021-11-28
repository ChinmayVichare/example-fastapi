"""add foreginkey to post table

Revision ID: d90c5c5b0ddb
Revises: 5187c503257c
Create Date: 2021-11-17 19:47:08.688774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd90c5c5b0ddb'
down_revision = '5187c503257c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table="users",local_cols=['owner_id'],remote_cols=['id'],
    ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')

    pass
