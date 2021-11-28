"""craete posts table

Revision ID: 9480f86c9511
Revises: 
Create Date: 2021-11-17 18:45:02.300423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import false


# revision identifiers, used by Alembic.
revision = '9480f86c9511'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
    ,sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts')
    pass
