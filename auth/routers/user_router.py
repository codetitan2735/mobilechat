from fastapi import APIRouter, Depends, Header

from dependencies.get_async_session import get_async_session
from schemas.user_schema import (
    UserRegisterSchema,
    UserLoginSchema,
    UserListSchema,
    UserRetrieveSchema,
    SuccessLoginSchema,
    UserRefreshTokensSchema
)
from services import user_service

user_router = APIRouter(prefix="/user")


@user_router.post("/", status_code=201)
async def register(user: UserRegisterSchema, session=Depends(get_async_session)):
    await user_service.create_user(user_data=user, session=session)
    return {}


@user_router.post("/token", status_code=200, response_model=SuccessLoginSchema)
async def login(login_data: UserLoginSchema, session=Depends(get_async_session)):
    tokens = await user_service.login_user(login_data=login_data, session=session)
    return tokens


@user_router.post("/token/refresh", status_code=200, response_model=SuccessLoginSchema)
async def refresh_tokens(refresh_token_schema: UserRefreshTokensSchema, session=Depends(get_async_session)):
    tokens = await user_service.refresh_tokens(
        refresh_token=refresh_token_schema.refresh_token,
        session=session
    )
    return tokens


@user_router.get("/{user_id}", response_model=UserRetrieveSchema)
async def get_user(user_id: str, session=Depends(get_async_session)):
    user = await user_service.get_user_by_id(user_id=user_id, session=session)
    return user


@user_router.get("/", response_model=UserListSchema)
async def get_users(session=Depends(get_async_session)):
    users = await user_service.get_users_list(session=session)
    return users


@user_router.get("token/validate")
async def validate_token(token: str = Header('')):
    token = token.replace('Bearer ', '')
    await user_service.validate_token(token=token, raise_exception=True)
    return {}
