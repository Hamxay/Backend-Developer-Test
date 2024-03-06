from injector import Binder, Module

from src.user import interfaces
from src.user.services.user_repository import UserRepository


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        """
        Configures bindings for the user module.

        This method is called by the injector framework to configure bindings for the user module.
        It binds the UserRepository interface to the concrete implementation UserRepository.

        :param binder: Binder instance for configuring bindings.
        """
        binder.bind(interfaces.UserRepository, UserRepository)  # type: ignore[type-abstract]
