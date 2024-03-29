"""empty message

Revision ID: 0ea5e1fd1304
Revises: f736efd4f952
Create Date: 2017-03-16 10:07:36.677716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea5e1fd1304'
down_revision = 'f736efd4f952'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('archived', sa.Boolean(), nullable=True))
    op.add_column('persons', sa.Column('archived', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('persons', 'archived')
    op.drop_column('companies', 'archived')
    # ### end Alembic commands ###
