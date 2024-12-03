from typing import Optional

from fastapi import Query, Header
from fastapi import status
from fastapi.websockets import WebSocket

from errors.base_http_exception import BaseHTTPException
from schemas.user_schema import RequestUserSchema
from services import user_service
from utils.jwt import decode_jwt_token_without_verification


async def get_user_from_websocket_token(websocket: WebSocket, token: Optional[str] = Query(None)) -> RequestUserSchema:
    """Return user data decoded from token or close websocket connection"""

    user_data = decode_jwt_token_without_verification(token=token)
    if user_data is None or not await user_service.is_token_valid(token=token):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        return RequestUserSchema(**user_data)


async def get_user_from_token(token: Optional[str] = Header(None)) -> RequestUserSchema:
    """Return user data decoded from token"""

    user_data = decode_jwt_token_without_verification(token=token)
    if user_data is None or not await user_service.is_token_valid(token=token):
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Valid token is required')
    else:
        return RequestUserSchema(**user_data)
