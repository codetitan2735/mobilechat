from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base


class BaseMixin:
    """
    Base mixin for each mixin with session and model_class
    """

    session: AsyncSession
    model_class: Base
