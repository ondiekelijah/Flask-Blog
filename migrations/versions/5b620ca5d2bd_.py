"""empty message

Revision ID: 5b620ca5d2bd
Revises: 0b61dc42c765
Create Date: 2020-10-24 13:06:08.796058

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5b620ca5d2bd'
down_revision = '0b61dc42c765'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('messo', sa.Text(), nullable=False))
    op.drop_column('messages', 'message')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('message', mysql.VARCHAR(length=2000), nullable=False))
    op.drop_column('messages', 'messo')
    # ### end Alembic commands ###
