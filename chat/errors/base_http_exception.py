class BaseHTTPException(Exception):
    """Custom exception with status code and detail info"""

    def __init__(self, status_code: int, detail: str = None) -> None:
        self.status_code = status_code
        self.detail = detail

    def __repr__(self) -> str:
        return self.detail
