from fastapi import APIRouter

from src.health.router import router as health_router
from src.user.router import router as rental_units_router


pre_router = APIRouter(
    prefix="/pre",
)
pre_router.include_router(health_router)
pre_router.include_router(rental_units_router)
