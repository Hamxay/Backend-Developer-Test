from fastapi import APIRouter

from src.post.router import router as post_router
from src.user.router import router as user_router


pre_router = APIRouter(
    prefix="/pre",
)
pre_router.include_router(post_router)
pre_router.include_router(user_router)
