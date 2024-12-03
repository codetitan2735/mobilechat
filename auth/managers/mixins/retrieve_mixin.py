from sqlalchemy.future import select

from db.base import Base
from managers.mixins.base_mixin import BaseMixin


class RetrieveMixin(BaseMixin):
    """
    Mixin to get by id
    """

    async def retrieve(self, pk: str) -> Base:
        query = select(self.model_class).where(self.model_class.id == pk)
        rows = await self.session.execute(query)
        return rows.scalars().first()
