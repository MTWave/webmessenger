from datetime import datetime, timedelta, timezone
from sqlite3 import IntegrityError
import sqlite3
from typing import Annotated, Union

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
from osiris.models.user_model import UserModel
from osiris.services.auth_service.exceptions import UserExistsException
from osiris.services.auth_service.models import TokenSchema, UserCreateSchema, UserJwtSchema

# to get a string like this run:
# openssl rand -hex 32

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def authentification_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    @staticmethod
    def create_token(user: UserModel) -> TokenSchema:
        user_data = UserJwtSchema(
            id=user.id,
            login=user.login
        )

        now_dttm = datetime.now(timezone.utc)
        payload = {
            "iat": now_dttm,
            "nbf": now_dttm,
            "exp": now_dttm + timedelta(seconds=settings.auth_service_expire_time),
            "sub": str(user_data.id),
            "user": user_data.model_dump()
        }
        token = jwt.encode(
            payload,
            key=settings.auth_service_jwt_secret,
            algorithm=settings.auth_service_jwt_algo
        )

        return TokenSchema(access_token=token)


    @staticmethod
    def validate_token(jwt_token: str) -> UserJwtSchema:
        try:
            payload = jwt.decode(
                jwt=jwt_token,
                key=settings.auth_service_jwt_secret,
                algorithms=[settings.auth_service_jwt_algo]
            )
        except jwt.exceptions.PyJWTError:
            raise AuthService.authentification_exception() from None

        user_data = payload.get("user")

        try:
            user = UserJwtSchema.model_validate(user_data)
        except ValidationError:
            raise AuthService.authentification_exception() from None

        return user

    async def register_new_user(self, user_data: UserCreateSchema) -> TokenSchema | None:

        user = UserModel(
            login=user_data.login,
            password=self.hash_password(user_data.password)
        )

        try:
            self.session.add(user)
            await self.session.commit()
        # ToDo
        except sqlalchemy.exc.IntegrityError: # DatabaseError
            raise UserExistsException()

        return self.create_token(user)

    async def authenticate_user(self, login: str, password: str) -> TokenSchema:
        user = await self.session.execute(
            select(UserModel).where(UserModel.login == login)
        )
        user = user.scalar()

        if not user or not self.verify_password(password, user.password):
            
            raise self.authentification_exception()

        return self.create_token(user)
