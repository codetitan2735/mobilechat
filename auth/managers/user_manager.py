from sqlalchemy.future import select

from db.models import User
from managers.base_manager import BaseManager
from managers.mixins import CreateMixin, ListMixin, RetrieveMixin


class UserManager(BaseManager, ListMixin, CreateMixin, RetrieveMixin):
    """
    Manager for User model
    """

    model_class = User
    
    async def get_by_username(self, username: str) -> User:
        query = select(self.model_class).where(self.model_class.username == username)
        rows = await self.session.execute(query)
        return rows.scalars().first()
