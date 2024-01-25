from injector import Inject

from src.core.db.client import DbClient
from src.core.use_cases import UseCase, UseCaseHandler


class CheckReadiness(UseCase):
    class Handler(UseCaseHandler["CheckReadiness", bool]):
        def __init__(
            self,
            db_client: Inject[DbClient],
        ) -> None:
            self._db_client = db_client

        async def execute(self, use_case: "CheckReadiness") -> bool:
            return await self._db_client.is_ready()
