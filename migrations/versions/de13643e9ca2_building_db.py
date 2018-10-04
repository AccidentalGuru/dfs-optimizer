"""building db

Revision ID: de13643e9ca2
Revises: 
Create Date: 2018-10-03 22:24:29.932503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de13643e9ca2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('abrev', sa.String(length=3), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_abrev'), 'team', ['abrev'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('position', sa.String(length=2), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_name'), 'player', ['name'], unique=False)
    op.create_index(op.f('ix_player_position'), 'player', ['position'], unique=False)
    op.create_table('player__game__stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('season', sa.Integer(), nullable=True),
    sa.Column('week', sa.Integer(), nullable=True),
    sa.Column('dropbacks', sa.Integer(), nullable=True),
    sa.Column('attempts', sa.Integer(), nullable=True),
    sa.Column('aimed', sa.Integer(), nullable=True),
    sa.Column('completions', sa.Integer(), nullable=True),
    sa.Column('passing_yds', sa.Integer(), nullable=True),
    sa.Column('passing_tds', sa.Integer(), nullable=True),
    sa.Column('passing_adot', sa.Float(), nullable=True),
    sa.Column('interceptions', sa.Integer(), nullable=True),
    sa.Column('sacks', sa.Integer(), nullable=True),
    sa.Column('completion_percentage', sa.Float(), nullable=True),
    sa.Column('adjusted_completion_percentage', sa.Float(), nullable=True),
    sa.Column('carries', sa.Integer(), nullable=True),
    sa.Column('rushing_yards', sa.Integer(), nullable=True),
    sa.Column('rushing_tds', sa.Integer(), nullable=True),
    sa.Column('rushing_fumbles', sa.Integer(), nullable=True),
    sa.Column('yds_per_carry', sa.Float(), nullable=True),
    sa.Column('yds_after_contact', sa.Float(), nullable=True),
    sa.Column('tackles_avoided', sa.Integer(), nullable=True),
    sa.Column('tackles_avoided_per_attempt', sa.Float(), nullable=True),
    sa.Column('targets', sa.Integer(), nullable=True),
    sa.Column('receptions', sa.Integer(), nullable=True),
    sa.Column('receiving_yds', sa.Integer(), nullable=True),
    sa.Column('receiving_tds', sa.Integer(), nullable=True),
    sa.Column('receiving_fumbles', sa.Integer(), nullable=True),
    sa.Column('receiving_adot', sa.Float(), nullable=True),
    sa.Column('drops', sa.Integer(), nullable=True),
    sa.Column('catch_percentage', sa.Float(), nullable=True),
    sa.Column('yds_per_reception', sa.Float(), nullable=True),
    sa.Column('yds_per_target', sa.Float(), nullable=True),
    sa.Column('receiving_yds_after_catch', sa.Float(), nullable=True),
    sa.Column('fantasy_points_standard', sa.Integer(), nullable=True),
    sa.Column('fantasy_points_ppr', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player__game__stats')
    op.drop_index(op.f('ix_player_position'), table_name='player')
    op.drop_index(op.f('ix_player_name'), table_name='player')
    op.drop_table('player')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_team_abrev'), table_name='team')
    op.drop_table('team')
    op.drop_table('blacklist_token')
    # ### end Alembic commands ###