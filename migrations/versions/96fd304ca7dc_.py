"""empty message

Revision ID: 96fd304ca7dc
Revises: 6c47c59b52bb
Create Date: 2020-10-17 10:03:29.128955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '96fd304ca7dc'
down_revision = '6c47c59b52bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('roles_ibfk_1', 'roles', type_='foreignkey')
    op.drop_column('roles', 'user_id')
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'user', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
    op.add_column('roles', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key('roles_ibfk_1', 'roles', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
