from sqlalchemy.ext.asyncio import AsyncSession

from db.config import async_session


async def get_async_session() -> AsyncSession:
    """Return async database session with started transaction"""

    async with async_session.begin() as session:
        yield session
