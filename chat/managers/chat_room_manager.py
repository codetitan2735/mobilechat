from db.models import ChatRoom
from managers.base_manager import BaseManager
from managers.mixins import ListMixin, RetrieveMixin, UpdateMixin, DeleteMixin, FilterMixin


class ChatRoomManager(BaseManager, ListMixin, RetrieveMixin, UpdateMixin, DeleteMixin, FilterMixin):
    """
    Manager for ChatRoom model
    """

    model_class = ChatRoom

    async def create(self, data: dict) -> ChatRoom:
        """Create chat room and return id of it"""

        new_user = self.model_class(**data)
        self.session.add(new_user)
        await self.session.flush()
        return new_user
