"""empty message

Revision ID: 4ac8791f5f7c
Revises: 455e1cca5e78
Create Date: 2020-10-16 11:42:26.572613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ac8791f5f7c'
down_revision = '455e1cca5e78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'user', ['role'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'permissions')
    # ### end Alembic commands ###
