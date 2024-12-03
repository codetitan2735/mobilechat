from fastapi import APIRouter

from routers.user_router import user_router


router = APIRouter()

router.include_router(router=user_router)

__all__ = ('router',)
