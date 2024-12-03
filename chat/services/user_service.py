import aiohttp
from fastapi import status

from errors.base_http_exception import BaseHTTPException
from schemas.user_schema import RequestUserSchema
from settings import AUTH_BACKEND_URL


def validate_user(user: RequestUserSchema, user_id: str, raise_exception: bool = False) -> bool:
    """Compare user id and raise BaseHTTPException if ids are not equal"""

    if str(user.id) == user_id:
        return True
    if raise_exception:
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User has no access to do this action')
    return False


async def is_token_valid(token: str) -> bool:
    """Validate token in auth backend server"""

    async with aiohttp.ClientSession() as session:
        async with session.get(AUTH_BACKEND_URL + 'token/validate',
                               headers={'Authorization': f'Bearer {token}'}) as response:
            return response.status == 200
