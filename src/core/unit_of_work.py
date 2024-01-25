from types import TracebackType
from typing import Self, Type

from injector import Inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.client import DbClient


class UnitOfWork:
    def __init__(
        self,
        db_client: Inject[DbClient],
    ) -> None:
        self._db_client = db_client

        self._db_session: AsyncSession | None = None

    async def get_db_session(self) -> AsyncSession:
        if not self._db_session:
            self._db_session = await self._db_client.create_session()

        return self._db_session

    async def flush(self) -> None:
        if self._db_session:
            await self._db_session.flush()

    async def commit(self) -> None:
        if self._db_session:
            await self._db_session.commit()

    async def rollback(self) -> None:
        if self._db_session:
            await self._db_session.rollback()

    async def close(self) -> None:
        if self._db_session:
            await self._db_session.close()
            self._db_session = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.close()
