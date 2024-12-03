from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from errors.base_http_exception import BaseHTTPException
from managers.user_manager import UserManager
from schemas.user_schema import SuccessLoginSchema, UserTokenPayloadSchema, UserLoginSchema, UserRetrieveSchema, \
    UserRegisterSchema, UserListSchema
from settings import ACCESS_TOKEN_EXPIRATION_TIMEDELTA, REFRESH_TOKEN_EXPIRATION_TIMEDELTA
from utils.jwt import generate_jwt_token, validate_jwt_token


def generate_tokens(token_user_payload: UserTokenPayloadSchema) -> SuccessLoginSchema:
    """Generate access and refresh tokens pair"""

    access_token = generate_jwt_token(
        payload=token_user_payload.dict(),
        expiration_timedelta=ACCESS_TOKEN_EXPIRATION_TIMEDELTA
    )
    refresh_token = generate_jwt_token(
        payload=token_user_payload.dict(),
        expiration_timedelta=REFRESH_TOKEN_EXPIRATION_TIMEDELTA
    )
    return SuccessLoginSchema(access_token=access_token, refresh_token=refresh_token)


async def refresh_tokens(refresh_token: str, session: AsyncSession) -> SuccessLoginSchema:
    """Generate new token pair if token is valid"""

    user_token_payload = validate_jwt_token(token=refresh_token)
    if user_token_payload:
        user_token_payload = UserTokenPayloadSchema(**user_token_payload)
    else:
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is not valid")
    user_manager = UserManager(session=session)
    user = await user_manager.get_by_username(username=user_token_payload.username)
    if not user:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return generate_tokens(token_user_payload=UserTokenPayloadSchema.from_orm(user))


async def login_user(login_data: UserLoginSchema, session: AsyncSession) -> SuccessLoginSchema:
    """Login user and generate tokens pair"""

    user_manager = UserManager(session=session)
    user = await user_manager.get_by_username(username=login_data.username)
    if not user:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user or user.password != login_data.password:
        raise BaseHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return generate_tokens(token_user_payload=UserTokenPayloadSchema.from_orm(user))


async def create_user(user_data: UserRegisterSchema, session: AsyncSession) -> None:
    """Create user"""

    user_manager = UserManager(session=session)
    await user_manager.create(data=user_data.dict())


async def get_user_by_id(user_id: str, session: AsyncSession) -> UserRetrieveSchema:
    """Get user by id"""

    user_manager = UserManager(session=session)
    user = await user_manager.retrieve(pk=user_id)
    if not user:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRetrieveSchema.from_orm(user)


async def get_users_list(session: AsyncSession) -> UserListSchema:
    """Return all users"""

    user_manager = UserManager(session=session)
    users = await user_manager.list()
    return UserListSchema.from_orm(users)


async def validate_token(token: str, raise_exception: bool = False) -> bool:
    """Validate token"""

    if validate_jwt_token(token=token):
        return True
    if raise_exception:
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token is not valid')
    return False
