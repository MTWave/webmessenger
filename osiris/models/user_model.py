from sqlalchemy import Column,  ForeignKey
import sqlalchemy.types as sqltp
from sqlalchemy.orm import relationship

from osiris.core.db import BaseDB

class UserModel(BaseDB):

    __tablename__ = "User"

    id =            Column(sqltp.Integer, primary_key=True, index=True)  
    login =         Column(sqltp.String(256), nullable=False)
    password =      Column(sqltp.String(256), nullable=False)

    # submitter = relationship("User", back_populates="recipes")  
    chats = relationship(
        "Chat",
        back_populates="users",
        uselist=True,
    )

    messages = relationship(
        "Message",
        back_populates="user",
        uselist=True,
    )
