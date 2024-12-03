import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models import User
from dependencies.get_async_session import get_async_session
from main import app
from schemas.user_schema import UserRegisterSchema
from settings import ASYNC_TEST_DB_URL

engine = create_async_engine(ASYNC_TEST_DB_URL, future=True)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_async_session() -> AsyncSession:
    """Return async database session with started transaction"""

    async with TestingSessionLocal.begin() as session:
        yield session


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the event loop for each test session."""

    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def create_test_database():
    """Create a clean database on every test session."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope='function')
def client() -> TestClient:
    """Return HTTP client and close it after test case"""

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='function')
async def session() -> AsyncSession:
    """Return async database session with started transaction"""

    async with TestingSessionLocal.begin() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
def user_data() -> dict:
    """Return dict with user data params"""

    return {
        'username': 'user21name',
        'password': 'pas12sword',
        'email': 'em23ail@email.email',
        'first_name': 'first name',
        'last_name': 'last name',
    }


@pytest.fixture(autouse=True)
async def user(session, user_data) -> User:
    """Create User in the database and return User instance"""

    create_user_data = UserRegisterSchema(**user_data)
    new_user = User(**create_user_data.dict())
    async with TestingSessionLocal.begin() as session:
        session.add(new_user)
        await session.commit()
        yield new_user
        await session.close()
