from fastapi.websockets import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from mongodb.schemas.message_schema import MessageSchema
from mongodb.services.mongodb_chat_room_service import upload_chat_room_message
from schemas.user_schema import RequestUserSchema
from services import chat_room_service


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user: RequestUserSchema, chat_room_id: str,
                      session: AsyncSession) -> None:
        if await chat_room_service.is_user_allowed_to_chat_room(user=user, chat_room_id=chat_room_id, session=session):
            await websocket.accept()
            if chat_room_id not in self.active_connections or not self.active_connections[chat_room_id]:
                self.active_connections[chat_room_id] = []
            self.active_connections[chat_room_id].append(websocket)
        else:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    def disconnect(self, websocket: WebSocket, chat_room_id: str) -> None:
        self.active_connections[chat_room_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str, chat_room_id: str) -> None:
        for connection in self.active_connections[chat_room_id]:
            await connection.send_text(message)


async def handle_chat_massage(manager: ConnectionManager, message: MessageSchema, chat_room_id: str) -> None:
    """Upload message to chat room storage and broadcast this message to every alive connection in chat room"""

    await upload_chat_room_message(chat_room_id=chat_room_id, message=message)
    await manager.broadcast(message=message.json(), chat_room_id=chat_room_id)
