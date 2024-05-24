"""Initial

Revision ID: f81ed92dbb64
Revises: 
Create Date: 2024-05-23 18:22:52.898702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# TODO:
# ==================================
# Adding link to models
# ==================================
# import  ???



# revision identifiers, used by Alembic.
revision: str = 'f81ed92dbb64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Message_id', table_name='Message')
    op.drop_table('Message')
    op.drop_index('ix_User_id', table_name='User')
    op.drop_table('User')
    op.drop_index('ix_Chat_id', table_name='Chat')
    op.drop_table('Chat')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Chat',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_Chat_id', 'Chat', ['id'], unique=False)
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('login', sa.VARCHAR(length=256), nullable=False),
    sa.Column('password', sa.VARCHAR(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_User_id', 'User', ['id'], unique=False)
    op.create_table('Message',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(length=256), nullable=False),
    sa.Column('creation_date', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_Message_id', 'Message', ['id'], unique=False)
    # ### end Alembic commands ###