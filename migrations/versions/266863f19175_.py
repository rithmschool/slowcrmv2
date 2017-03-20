"""empty message

Revision ID: 266863f19175
Revises: 0ea5e1fd1304
Create Date: 2017-03-20 13:19:54.480556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '266863f19175'
down_revision = '0ea5e1fd1304'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('persons_email_key', 'persons', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('persons_email_key', 'persons', ['email'])
    # ### end Alembic commands ###
