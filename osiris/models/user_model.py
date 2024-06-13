from sqlalchemy import Column,  ForeignKey
import sqlalchemy.types as sqltp
from sqlalchemy.orm import relationship, Mapped

from osiris.core.db import BaseDB

from osiris.models.users_chats_model import UsersChatsModel

class UserModel(BaseDB):

    __tablename__ = "User"

    id =            Column(sqltp.Integer, primary_key=True, index=True)  
    login =         Column(sqltp.String(256), nullable=False, unique=True)
    password =      Column(sqltp.String(256), nullable=False)

    # submitter = relationship("User", back_populates="recipes")
    chats = relationship(
        "ChatModel",
        secondary="Users_Chats",
        # many-to-one relationship
        primaryjoin=("UserModel.id == UsersChatsModel.user_id"),
        # many-to-many relationship
        secondaryjoin=("ChatModel.id == UsersChatsModel.chat_id"),
        back_populates="members",
        uselist=True,
    )

