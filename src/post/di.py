from injector import Binder, Module

from src.post import interface
from src.post.services.post_repository import PostRepository


class PostModule(Module):
    def configure(self, binder: Binder) -> None:
        """
        Configures bindings for the PostModule.

        This method binds the PostRepository interface to the PostRepository implementation.

        Parameters:
        - binder (Binder): The injector binder used for binding implementations to interfaces.
        """
        binder.bind(interface.PostRepository, PostRepository)  # type: ignore[type-abstract]
