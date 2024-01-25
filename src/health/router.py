from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from fastapi_injector import Injected

from src.health.use_cases import CheckLiveness, CheckReadiness


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/live",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Check if the service is alive",
    responses={
        204: {"description": "Service available"},
        503: {"description": "Service unavailable"},
    },
)
async def check_liveness(
    use_case: Annotated[CheckLiveness, Depends()],
    handler: Annotated[CheckLiveness.Handler, Injected(CheckLiveness.Handler)],
) -> Response:
    if await handler.execute(use_case):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.get(
    "/ready",
    description="Check if the service is ready to accept requests",
    responses={
        204: {"description": "Service ready"},
        503: {"description": "Service not ready"},
    },
)
async def check_readiness(
    use_case: Annotated[CheckReadiness, Depends()],
    handler: Annotated[CheckReadiness.Handler, Injected(CheckReadiness.Handler)],
) -> Response:
    if await handler.execute(use_case):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
