"""empty message

Revision ID: 28caa9ef58ed
Revises: 19b640542718
Create Date: 2017-03-16 13:36:23.196492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28caa9ef58ed'
down_revision = '19b640542718'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('companies', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.create_unique_constraint(None, 'companies', ['id'])
    op.create_unique_constraint(None, 'persons', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'persons', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    op.alter_column('companies', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###
