from fastapi import APIRouter

from routers.chat_room_router import chat_room_router
from routers.chat_router import chat_router
from routers.graphql_router import graphql_router

router = APIRouter()

router.include_router(router=chat_room_router)
router.include_router(router=chat_router)
router.include_router(router=graphql_router)

__all__ = ('router',)
