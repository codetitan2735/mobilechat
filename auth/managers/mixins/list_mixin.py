from sqlalchemy.future import select

from db.base import Base
from managers.mixins.base_mixin import BaseMixin


class ListMixin(BaseMixin):
    """
    Mixin to get list of table rows
    """

    async def list(self) -> list[Base]:
        query = select(self.model_class)
        rows = await self.session.execute(query)
        return rows.scalars().all()
