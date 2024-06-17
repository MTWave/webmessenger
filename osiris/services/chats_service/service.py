from datetime import datetime, timedelta, timezone
import logging
from sqlite3 import IntegrityError
import sqlite3
from typing import Annotated, List, Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, logger, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlalchemy import select
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession


from osiris import settings
from osiris.core.db import get_session
from osiris.models.chat_model import ChatModel
from osiris.models.message_model import MessageModel
from osiris.models.user_model import UserModel
from osiris.models.users_chats_model import UsersChatsModel
from osiris.services.auth_service.exceptions import UserExistsException
from osiris.services.auth_service.models import TokenSchema, UserCreateSchema, UserJwtSchema
from osiris.services.chats_service.models import ChatBriefSchema


logger = logging.getLogger("custom")


class ChatService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_chats_by_user_id(self, user_id) -> List[ChatModel]:
        query = (
            select(ChatModel)
                .join(UsersChatsModel)
                .filter(UsersChatsModel.user_id == user_id)
        )

        result = await self.session.execute(query)
        r = result.scalars().all()
        logger.info(r)
        return r


    async def get_messages_by_chat_id(self, chat_id,user_id) -> List[MessageModel]:
        query = (
            select(MessageModel)
                .join(UsersChatsModel, MessageModel.chat_id == UsersChatsModel.chat_id)
                .join(UserModel, MessageModel.user_id == UserModel.id)
                .filter(UsersChatsModel.user_id == user_id)
                .filter(ChatModel.id == chat_id)
        )

        result = await self.session.execute(query)
        r = result.scalars().all()
        logger.info([a for a in r])
        return r

    #ToDO check chat exists , user in chat exists
    async def create_message(
        self,
        chat_id,
        user_id,
        message_text
    ) -> None:
        message = MessageModel(
            content=message_text,
            creation_date=datetime.now(),
            chat_id=chat_id,
            user_id=user_id
        )

        self.session.add(message)
        await self.session.commit()
        # ToDo


