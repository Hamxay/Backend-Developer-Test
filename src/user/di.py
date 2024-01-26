from injector import Binder, Module

from src.user import interfaces
from src.user.services.user_repository import (
    UserRepository,
)


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.UserRepository, UserRepository)  # type: ignore[type-abstract]
