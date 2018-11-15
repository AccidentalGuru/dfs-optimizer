"""Add File table

Revision ID: ec185c3722e4
Revises: 8ef520b2c652
Create Date: 2018-11-13 22:17:32.996231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec185c3722e4'
down_revision = '8ef520b2c652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(length=64), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    # ### end Alembic commands ###