from sqlalchemy import delete

from managers.mixins.base_mixin import BaseMixin


class DeleteMixin(BaseMixin):
    """
    Mixin to create model row in db
    """

    async def delete(self, pk: str) -> None:
        query = delete(self.model_class).where(self.model_class.id == pk)
        await self.session.execute(query)
        await self.session.flush()
