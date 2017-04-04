"""empty message

Revision ID: f4facdc48ee0
Revises: 478831377966
Create Date: 2017-03-30 16:49:06.519393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4facdc48ee0'
down_revision = '478831377966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('archived', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'archived')
    # ### end Alembic commands ###
