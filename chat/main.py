import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from error_handlers.base_http_exception_handler import base_http_exception_handler
from errors.base_http_exception import BaseHTTPException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from routers import router

app = FastAPI()
app.include_router(router=router)

app.add_exception_handler(BaseHTTPException, base_http_exception_handler)

origins = [
    "http://localhost",
    "http://localhost:19000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
