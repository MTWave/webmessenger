import logging
from optparse import Option
from typing import Optional
from fastapi import Depends, HTTPException, Request, WebSocket
from pydantic import ValidationError

from osiris.services.auth_service.models import UserJwtSchema
from osiris.services.auth_service.auth_service import AuthService, oauth2_scheme

from osiris import settings

async def check_current_user(token: str = Depends(oauth2_scheme)) -> UserJwtSchema:
    return AuthService.validate_token(token)


async def get_current_user_ws(request: WebSocket) -> Optional[UserJwtSchema]:
    access_token = request.cookies.get(settings.auth_service_cookie_name)
    try:
        # ToDo Bearer access_token= - dirty hack!
        if access_token is not None and access_token.startswith("Bearer"):
            access_token = access_token.removeprefix("Bearer").strip()
            return AuthService.validate_token(access_token)

    except (ValidationError, HTTPException):
        pass

    return None

async def get_current_user(request: Request) -> Optional[UserJwtSchema]:
    access_token = request.cookies.get(settings.auth_service_cookie_name)
    try:
        # ToDo Bearer access_token= - dirty hack!
        if access_token is not None and access_token.startswith("Bearer"):
            access_token = access_token.removeprefix("Bearer").strip()
            return AuthService.validate_token(access_token)

    except (ValidationError, HTTPException):
        pass

    return None
