from typing import Optional

from fastapi.encoders import jsonable_encoder

from mongodb.config import mongo_chat_db
from mongodb.models.mongodb_chat_room import ChatRoomModel, MessageModel
from mongodb.schemas.message_schema import MessageSchema


async def create_chat_room_mongodb(origin_chat_room_id: str) -> Optional[str]:
    """Create chat room record"""

    chat_room = ChatRoomModel(origin_chat_room_id=origin_chat_room_id, messages=[])
    chat_room = jsonable_encoder(chat_room)
    new_chat_room = await mongo_chat_db['chat_rooms'].insert_one(chat_room)
    created_chat_room = await mongo_chat_db['chat_rooms'].find_one({'_id': new_chat_room.inserted_id})
    return created_chat_room.get('_id', None)


async def get_chat_room_messages(chat_room_id: str) -> list[MessageModel]:
    """Get chat room messages"""

    chat_room = await mongo_chat_db['chat_rooms'].find_one({'origin_chat_room_id': chat_room_id})
    chat_room = ChatRoomModel(**chat_room)
    return chat_room.messages


async def upload_chat_room_message(chat_room_id: str, message: MessageSchema) -> None:
    """Upload message to chat room messages"""

    message = MessageModel(**message.dict())
    message = jsonable_encoder(message)
    await mongo_chat_db['chat_rooms'].update_one(
        {'origin_chat_room_id': chat_room_id},
        {'$push': {'messages': message}}
    )
