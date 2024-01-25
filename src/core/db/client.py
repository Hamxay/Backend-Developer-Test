from asyncio import current_task

from asyncpg.exceptions import PostgresError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)


class DbClient:
    def __init__(self, url: str, echo: bool = False) -> None:
        self._engine = create_async_engine(url, echo=echo)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                bind=self._engine,
                autocommit=False,
                expire_on_commit=False,
            ),
            current_task,
        )

    async def is_ready(self) -> bool:
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("select 1"))
                return True
        except (
            ConnectionRefusedError,
            SQLAlchemyError,
            PostgresError,
        ):
            return False

    async def create_session(self) -> AsyncSession:
        return self._session_factory()
