from injector import Binder, Module

from src.post import interface
from src.post.services.post_repository import (
    PostRepository,
)


class PostModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface.PostRepository, PostRepository)  # type: ignore[type-abstract]
