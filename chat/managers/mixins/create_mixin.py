from managers.mixins.base_mixin import BaseMixin


class CreateMixin(BaseMixin):
    """
    Mixin to create model row in db
    """

    async def create(self, data: dict) -> None:
        new_user = self.model_class(**data)
        self.session.add(new_user)
        await self.session.flush()
