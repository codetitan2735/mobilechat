from starlette.requests import Request
from starlette.responses import JSONResponse

from errors.base_http_exception import BaseHTTPException


def base_http_exception_handler(request: Request, exc: BaseHTTPException):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})
