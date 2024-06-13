"""initial

Revision ID: 39e874cef2d0
Revises: 
Create Date: 2024-06-13 19:05:25.798790

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
revision: str = '39e874cef2d0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Chat_id'), 'Chat', ['id'], unique=False)
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_index(op.f('ix_User_id'), 'User', ['id'], unique=False)
    op.create_table('Message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=256), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['Chat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Message_id'), 'Message', ['id'], unique=False)
    op.create_table('Users_Chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['Chat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Users_Chats_id'), 'Users_Chats', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Users_Chats_id'), table_name='Users_Chats')
    op.drop_table('Users_Chats')
    op.drop_index(op.f('ix_Message_id'), table_name='Message')
    op.drop_table('Message')
    op.drop_index(op.f('ix_User_id'), table_name='User')
    op.drop_table('User')
    op.drop_index(op.f('ix_Chat_id'), table_name='Chat')
    op.drop_table('Chat')
    # ### end Alembic commands ###
