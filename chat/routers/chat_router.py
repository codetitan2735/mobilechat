from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect

from dependencies.get_async_session import get_async_session
from dependencies.get_user_token import get_user_from_websocket_token
from mongodb.schemas.message_schema import MessageSchema
from schemas.user_schema import RequestUserSchema
from services.chat_service import ConnectionManager, handle_chat_massage

chat_router = APIRouter(prefix="/chat")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            const access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsImlkIjoiMDNjOWNmNTUtYTdjYS00MTMxLTk2NjItMTVkYWRiZTc5OTU5IiwiZXhwIjoxNjI2MTY3MTMxfQ.tj_W1pm8S6JXwBBWIIU3IkguXX9eK57HjibXPEvAZyY'
            const chat_room_id = 'f12cdffb-a648-40f3-a629-b59416d9c645'
            var ws = new WebSocket(`ws://localhost:8001/chat/${chat_room_id}/ws?token=${access_token}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                const data = {text: input.value, timestamp: Date.now()}
                ws.send(JSON.stringify(data))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@chat_router.get("/")
async def get():
    return HTMLResponse(html)


manager = ConnectionManager()


@chat_router.websocket("/chat/{chat_room_id}/ws")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_room_id: str,
        user: RequestUserSchema = Depends(get_user_from_websocket_token),
        session=Depends(get_async_session)
):
    if not user:
        return
    await manager.connect(websocket=websocket, user=user, chat_room_id=chat_room_id, session=session)
    try:
        while True:
            message = await websocket.receive_json()
            message = MessageSchema(author_id=user.id, **message)
            await handle_chat_massage(manager=manager, message=message, chat_room_id=chat_room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket, chat_room_id=chat_room_id)
