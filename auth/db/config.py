from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import ASYNC_DATABASE_URL

engine = create_async_engine(ASYNC_DATABASE_URL)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
