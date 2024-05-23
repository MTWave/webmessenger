from sqlalchemy import Column,  ForeignKey
import sqlalchemy.types as sqltp
from sqlalchemy.orm import relationship

from osiris.core.db import BaseDB

class ChatModel(BaseDB):

    __tablename__ = "Chat"

    id =            Column(sqltp.Integer, primary_key=True, index=True)  
    name =          Column(sqltp.String(256), nullable=False)

    messages = relationship(
        "Message",
        cascade="all,delete-orphan",
        back_populates="chat_id",
        uselist=True,
    )
    users = relationship(
        "User",
        back_populates="chats",
        uselist=True,
    )
