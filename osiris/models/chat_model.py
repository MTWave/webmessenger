from sqlalchemy import Column,  ForeignKey
import sqlalchemy.types as sqltp
from sqlalchemy.orm import relationship

from osiris.core.db import BaseDB

class ChatModel(BaseDB):

    __tablename__ = "Chat"

    id =            Column(sqltp.Integer, primary_key=True, index=True)  
    name =          Column(sqltp.String(256), nullable=False)

    messages = relationship(
        "MessageModel",
        back_populates="chat",
        uselist=True,
    )

    members = relationship(
        "UserModel",
        secondary="Users_Chats",
        # many-to-one relationship
        primaryjoin=("ChatModel.id == UsersChatsModel.chat_id"),
        # many-to-many relationship
        secondaryjoin=("UserModel.id == UsersChatsModel.user_id"),
        back_populates="chats",
        uselist=True,
    )
