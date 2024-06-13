from fastapi import Depends

from osiris.services.auth_service.models import UserJwtSchema
from osiris.services.auth_service.auth_service import AuthService, oauth2_scheme


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserJwtSchema:
    return AuthService.validate_token(token)
