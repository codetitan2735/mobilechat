from typing import Optional

import jwt


def decode_jwt_token_without_verification(token: str) -> Optional[dict]:
    """Return jwt token payload after decode without secret key section check"""

    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.DecodeError:
        return None
