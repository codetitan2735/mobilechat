from datetime import timedelta, datetime
from typing import Optional

import jwt

from settings import SECRET_KEY


def generate_jwt_token(payload: dict, expiration_timedelta: int) -> str:
    """Return jwt token with payload and expiration time"""

    payload['exp'] = datetime.utcnow() + timedelta(seconds=expiration_timedelta)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validate_jwt_token(token: str) -> Optional[dict]:
    """Try to decode token to validate it"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.DecodeError:
        return None
