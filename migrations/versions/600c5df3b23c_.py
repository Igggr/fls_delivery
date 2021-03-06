"""empty message

Revision ID: 600c5df3b23c
Revises: 5aa21d6539bd
Create Date: 2020-02-23 20:09:49.844533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '600c5df3b23c'
down_revision = '5aa21d6539bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('_status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', '_status')
    # ### end Alembic commands ###
