from typing import Awaitable, Callable
from injector import Injector

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.core.unit_of_work import UnitOfWork


class UnitOfWorkMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, injector: Injector) -> None:
        super().__init__(app)
        self._injector = injector

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        async with self._injector.get(UnitOfWork) as unit_of_work:
            response = await call_next(request)
            if response.status_code >= 400:
                await unit_of_work.rollback()

            return response
