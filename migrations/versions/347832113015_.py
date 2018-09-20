"""empty message

Revision ID: 347832113015
Revises: 1bfc808a2677
Create Date: 2018-07-30 23:56:47.821384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '347832113015'
down_revision = '1bfc808a2677'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player__game__stats', sa.Column('season', sa.Integer(), nullable=True))
    op.add_column('player__game__stats', sa.Column('week', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('player__game__stats', 'week')
    op.drop_column('player__game__stats', 'season')
    # ### end Alembic commands ###
