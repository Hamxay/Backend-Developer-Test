from fastapi_injector import request_scope
from injector import (
    Binder,
    Module,
    provider,
    singleton,
)

from src.core.db.client import DbClient
from src.core.unit_of_work import UnitOfWork
from src.settings import (
    DB_ECHO,
    DB_URL,
)


class CoreModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(UnitOfWork, scope=request_scope)

    @singleton
    @provider
    def provide_db_client(self) -> DbClient:
        return DbClient(DB_URL, DB_ECHO)
