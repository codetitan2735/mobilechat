from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from errors.base_http_exception import BaseHTTPException
from managers.chat_room_manager import ChatRoomManager
from schemas.chat_room_schema import (
    CreateChatRoomSchema,
    ListChatRoomSchema,
    DetailChatRoomSchema,
    UpdateChatRoomMembersSchema
)
from schemas.user_schema import RequestUserSchema
from mongodb.services import mongodb_chat_room_service
from services import user_service


async def create_chat_room(chat_room_data: CreateChatRoomSchema, session: AsyncSession,
                           user: RequestUserSchema) -> None:
    """Create chat room"""

    user_service.validate_user(user=user, user_id=str(chat_room_data.creator), raise_exception=True)
    chat_room_manager = ChatRoomManager(session=session)
    chat_room = await chat_room_manager.create(data=chat_room_data.dict())
    await mongodb_chat_room_service.create_chat_room_mongodb(origin_chat_room_id=str(chat_room.id))


async def get_chat_rooms_list(session: AsyncSession, user: RequestUserSchema) -> ListChatRoomSchema:
    """Get all chat rooms"""

    chat_room_manager = ChatRoomManager(session=session)
    chat_rooms = await chat_room_manager.filter(creator=str(user.id))
    return ListChatRoomSchema.from_orm(chat_rooms)


async def get_chat_room_by_id(chat_room_id: str, session: AsyncSession,
                              user: RequestUserSchema) -> DetailChatRoomSchema:
    """Get all chat rooms"""

    chat_room_manager = ChatRoomManager(session=session)
    chat_room = await chat_room_manager.filter_one(id=chat_room_id, members__contains=str(user.id))
    if not chat_room:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Chat room is not found')
    return DetailChatRoomSchema.from_orm(chat_room)


async def update_chat_room_members(chat_room_id: str, update_data: UpdateChatRoomMembersSchema,
                                   session: AsyncSession, user: RequestUserSchema) -> None:
    """Update chat room members field"""

    await update_chat_room(chat_room_id=chat_room_id, update_data=update_data.dict(), session=session, user=user)


async def update_chat_room(chat_room_id: str, update_data: dict, session: AsyncSession,
                           user: RequestUserSchema) -> None:
    """Update chat room"""

    chat_room_manager = ChatRoomManager(session=session)
    if await is_user_admin_of_chat_room(user=user, chat_room_id=chat_room_id, session=session):
        await chat_room_manager.update(pk=chat_room_id, data=update_data)


async def is_user_allowed_to_chat_room(user: RequestUserSchema, chat_room_id: id, session: AsyncSession) -> bool:
    """Check if user in members of chat room"""

    chat_room_manager = ChatRoomManager(session=session)
    chat_room = await chat_room_manager.filter_one(id=chat_room_id, members__contains=str(user.id))
    return chat_room is not None


async def is_user_admin_of_chat_room(user: RequestUserSchema, chat_room_id: id, session: AsyncSession) -> bool:
    """Check if user is admin of chat room"""

    chat_room_manager = ChatRoomManager(session=session)
    chat_room = await chat_room_manager.filter_one(id=chat_room_id, creator=str(user.id))
    return chat_room is not None
