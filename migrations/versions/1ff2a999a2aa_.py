"""empty message

Revision ID: 1ff2a999a2aa
Revises: 97169a946927
Create Date: 2021-03-22 18:48:02.720817

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1ff2a999a2aa'
down_revision = '97169a946927'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('replies', 'comment_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_constraint('replies_ibfk_1', 'replies', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('replies_ibfk_1', 'replies', 'comments', ['comment_id'], ['id'], ondelete='SET NULL')
    op.alter_column('replies', 'comment_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###
