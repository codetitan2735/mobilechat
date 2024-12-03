from hashlib import sha256


def hash_string(value: str) -> str:
    """Hash string with sha256 algorithm"""
    return sha256(value.encode()).hexdigest()
