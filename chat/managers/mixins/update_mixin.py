from sqlalchemy import update

from managers.mixins.base_mixin import BaseMixin


class UpdateMixin(BaseMixin):
    """
    Mixin to update model row in db
    """

    async def update(self, pk: str, data: dict) -> None:
        query = update(self.model_class).where(self.model_class.id == pk).values(**data)
        await self.session.execute(query)
        await self.session.flush()
