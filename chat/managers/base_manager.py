from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base


class BaseManager:
    """
    Base manager for each model manager with database session
    """

    model_class: Base = None

    def __init__(self, session: AsyncSession):
        self.session = session
