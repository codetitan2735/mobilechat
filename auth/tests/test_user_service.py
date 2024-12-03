import pytest

from schemas.user_schema import UserLoginSchema, UserRegisterSchema, UserTokenPayloadSchema
from services import user_service
from tests.conftest import TestingSessionLocal


def test_generate_tokens():
    tokens = user_service.generate_tokens(token_user_payload=UserTokenPayloadSchema(
        username='username',
        id='03c9cf55-a7ca-4131-9662-15dadbe79959',
    ))
    assert tokens.access_token
    assert tokens.refresh_token


@pytest.mark.asyncio
async def test_login_user(session, user_data):
    login_data = UserLoginSchema(**user_data)
    tokens = await user_service.login_user(login_data=login_data, session=session)
    assert tokens.access_token
    assert tokens.refresh_token


@pytest.fixture(scope='function')
async def refresh_token(user_data) -> str:
    login_data = UserLoginSchema(**user_data)
    async with TestingSessionLocal.begin() as session:
        tokens = await user_service.login_user(login_data=login_data, session=session)
    return tokens.refresh_token


@pytest.mark.asyncio
async def test_refresh_tokens(session, refresh_token):
    tokens = await user_service.refresh_tokens(refresh_token=refresh_token, session=session)
    assert tokens.access_token
    assert tokens.refresh_token


@pytest.mark.asyncio
async def test_create_user(session):
    create_user_data = {
        'username': 'username',
        'password': 'password',
        'email': 'test@email.email',
        'first_name': 'first name',
        'last_name': 'last name',
    }
    create_user_data = UserRegisterSchema(**create_user_data)
    await user_service.create_user(user_data=create_user_data, session=session)


@pytest.mark.asyncio
async def test_get_user_by_id(session, user):
    response_user = await user_service.get_user_by_id(user_id=user.id, session=session)
    assert user.id == response_user.id
    assert user.username == response_user.username


@pytest.mark.asyncio
async def test_get_user_by_id(session, user):
    users_list = await user_service.get_users_list(session=session)
    assert user.id in [u.id for u in users_list.__root__]
