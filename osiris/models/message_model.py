from sqlalchemy import Column,  ForeignKey
import sqlalchemy.types as sqltp
from sqlalchemy.orm import relationship

from osiris.core.db import BaseDB

class MessageModel(BaseDB):

    __tablename__ = "Message"

    id =            Column(sqltp.Integer, primary_key=True, index=True)

    content =       Column(sqltp.String(256), nullable=False)
    # ToDo: attachments?
    creation_date = Column(sqltp.DateTime, nullable=False)

    chat_id = Column(sqltp.Integer, ForeignKey("Chat.id"), nullable=True)
    chat   = relationship("Chat", back_populates="messages")

    user_id = Column(sqltp.Integer, ForeignKey("User.id"), nullable=True)
    user   = relationship("User", back_populates="messages")
