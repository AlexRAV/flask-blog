"""empty message

Revision ID: b20a2f7424eb
Revises: e4b5a841ee60
Create Date: 2017-01-15 23:37:45.550696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b20a2f7424eb'
down_revision = 'e4b5a841ee60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('profiles_user_fkey', 'profiles', type_='foreignkey')
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'])
    op.drop_column('profiles', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.create_foreign_key('profiles_user_fkey', 'profiles', 'users', ['user'], ['id'])
    op.drop_column('profiles', 'user_id')
    # ### end Alembic commands ###
