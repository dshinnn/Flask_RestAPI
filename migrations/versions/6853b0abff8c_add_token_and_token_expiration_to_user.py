"""Add token and token expiration to User

Revision ID: 6853b0abff8c
Revises: ebf01902bdfb
Create Date: 2022-02-02 11:31:44.897313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6853b0abff8c'
down_revision = 'ebf01902bdfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###
