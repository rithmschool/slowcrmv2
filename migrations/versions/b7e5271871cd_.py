"""empty message

Revision ID: b7e5271871cd
Revises: 478831377966
Create Date: 2017-03-24 11:54:37.210392

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'b7e5271871cd'
down_revision = '478831377966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_companies_search_vector', 'companies', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('entries', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_entries_search_vector', 'entries', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('persons', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_persons_search_vector', 'persons', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('tags', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_tags_search_vector', 'tags', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('users', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_users_search_vector', 'users', ['search_vector'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_search_vector', table_name='users')
    op.drop_column('users', 'search_vector')
    op.drop_index('ix_tags_search_vector', table_name='tags')
    op.drop_column('tags', 'search_vector')
    op.drop_index('ix_persons_search_vector', table_name='persons')
    op.drop_column('persons', 'search_vector')
    op.drop_index('ix_entries_search_vector', table_name='entries')
    op.drop_column('entries', 'search_vector')
    op.drop_index('ix_companies_search_vector', table_name='companies')
    op.drop_column('companies', 'search_vector')
    # ### end Alembic commands ###
