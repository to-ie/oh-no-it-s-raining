"""loc table

Revision ID: 962ce055e29d
Revises: b2924f9e00c2
Create Date: 2022-11-24 19:51:49.154103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '962ce055e29d'
down_revision = 'b2924f9e00c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=140), nullable=True),
    sa.Column('area', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loc')
    # ### end Alembic commands ###
