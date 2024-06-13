from sqlalchemy import Column,  ForeignKey
import sqlalchemy.types as sqltp
from sqlalchemy.orm import relationship

from osiris.core.db import BaseDB


class UsersChatsModel(BaseDB):
    __tablename__ = 'Users_Chats'

    id      = Column(sqltp.Integer, primary_key=True, index=True)  
    user_id = Column(sqltp.Integer, ForeignKey('User.id'))
    chat_id = Column(sqltp.Integer, ForeignKey('Chat.id'))
