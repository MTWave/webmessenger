from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm


from osiris import settings
from osiris.schemas.exception import ExceptionMessageSchema
from osiris.services.auth_service.auth_service import AuthService
from osiris.services.auth_service.exceptions import UserExistsException
from osiris.services.auth_service.models import TokenSchema, UserCreateSchema, UserLoginSchema


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# ToDo: method to service?
def set_auth_token(response: Response, access_token: TokenSchema):
    response.set_cookie(
        key=settings.auth_service_cookie_name, 
        value=f"Bearer {access_token.access_token}",
        httponly=True
    )  
    return access_token


@router.post(
    "/sign_up",
    response_model=TokenSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": TokenSchema,
            "description": "Successfully created a new account"
        },
        status.HTTP_409_CONFLICT: {
            "model": ExceptionMessageSchema,
            "description": "User with this email already exists"
        }
    }
)
async def sign_up(
    response: Response, 
    user_data: UserCreateSchema,
    service: AuthService = Depends()
):
    """
    Create a new account

    **user_data**: username, email and password for registration
    """
    try:
        access_token = await service.register_new_user(user_data)
    except UserExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    return set_auth_token(response, access_token)

@router.post(
    "/sign_in",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": TokenSchema,
            "description": "Successful login"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ExceptionMessageSchema,
            "description": "Could not validate credentials"
        }
    }
)
async def sign_in(
        # ToDo: OAuth2PasswordRequestForm
        #form_data: OAuth2PasswordRequestForm = Depends(),
        response: Response,
        user_data: UserCreateSchema,
        service: AuthService = Depends()
):
    """
    Authorization

    **form_data**: password and email for authorization
    """
    access_token = await service.authenticate_user(
        user_data.login,
        user_data.password
    )

    return set_auth_token(response, access_token)
