from fastapi import APIRouter, Depends

from dependencies.get_async_session import get_async_session
from dependencies.get_user_token import get_user_from_token
from schemas.chat_room_schema import CreateChatRoomSchema, ListChatRoomSchema, UpdateChatRoomNameSchema, \
    UpdateChatRoomMembersSchema, DetailChatRoomSchema
from schemas.user_schema import RequestUserSchema
from services import chat_room_service

chat_room_router = APIRouter(prefix='/chat/room')


@chat_room_router.post('', status_code=201)
async def create(chat_room_data: CreateChatRoomSchema, session=Depends(get_async_session),
                 user: RequestUserSchema = Depends(get_user_from_token)):

    await chat_room_service.create_chat_room(chat_room_data=chat_room_data, session=session, user=user)
    return {}


@chat_room_router.get('', response_model=ListChatRoomSchema)
async def get_chat_rooms(session=Depends(get_async_session), user: RequestUserSchema = Depends(get_user_from_token)):

    chat_rooms = await chat_room_service.get_chat_rooms_list(session=session, user=user)
    return chat_rooms


@chat_room_router.get('/{chat_room_id}', response_model=DetailChatRoomSchema)
async def get_chat_room(chat_room_id: str, session=Depends(get_async_session),
                        user: RequestUserSchema = Depends(get_user_from_token)):

    chat_room = await chat_room_service.get_chat_room_by_id(chat_room_id=chat_room_id, session=session, user=user)
    return chat_room


@chat_room_router.put('/{chat_room_id}/name')
async def update_chat_room_name(
        chat_room_id: str,
        update_data: UpdateChatRoomNameSchema,
        session=Depends(get_async_session),
        user: RequestUserSchema = Depends(get_user_from_token)
):

    await chat_room_service.update_chat_room(
        chat_room_id=chat_room_id,
        update_data=update_data.dict(),
        session=session,
        user=user
    )
    return {}


@chat_room_router.put('/{chat_room_id}/members')
async def update_chat_room_members(
        chat_room_id: str,
        update_data: UpdateChatRoomMembersSchema,
        session=Depends(get_async_session),
        user: RequestUserSchema = Depends(get_user_from_token)
):

    await chat_room_service.update_chat_room_members(
        chat_room_id=chat_room_id,
        update_data=update_data,
        session=session,
        user=user
    )
    return {}
