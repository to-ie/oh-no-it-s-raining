"""loc table

Revision ID: f4f97dac523a
Revises: 9f06173ee918
Create Date: 2022-11-24 15:59:37.804394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4f97dac523a'
down_revision = '9f06173ee918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.drop_column('location')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.VARCHAR(length=140), nullable=True))

    # ### end Alembic commands ###