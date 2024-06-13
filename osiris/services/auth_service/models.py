from typing import Optional, List

from pydantic import BaseModel, validator


class UserJwtSchema(BaseModel):
    login: str
    id: int

class UserCreateSchema(BaseModel):
    login: str
    password: str

class UserLoginSchema(UserCreateSchema):
    pass

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

