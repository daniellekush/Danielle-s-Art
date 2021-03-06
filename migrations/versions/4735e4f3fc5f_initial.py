"""initial

Revision ID: 4735e4f3fc5f
Revises: 
Create Date: 2021-12-05 23:24:39.780202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4735e4f3fc5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Suggestion',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sType', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('desc', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('PageSuggestion',
    sa.Column('suggestion', sa.Integer(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['User.id'], ),
    sa.ForeignKeyConstraint(['suggestion'], ['Suggestion.id'], ),
    sa.PrimaryKeyConstraint('suggestion')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PageSuggestion')
    op.drop_table('User')
    op.drop_table('Suggestion')
    # ### end Alembic commands ###
