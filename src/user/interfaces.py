from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from src.user.models import User
from src.user.schemas import ResponseUserSchema


@runtime_checkable
class UserRepository(Protocol):
    async def get_by_id(self, user_id: str) -> ResponseUserSchema | None:
        ...

    async def get_list(self) -> Sequence[ResponseUserSchema]:
        ...

    async def create(
        self,
        user: User,
    ) -> None:
        ...

    async def save(
        self,
        user: User,
    ) -> None:
        ...

    async def delete_by_id(
        self,
        user_id: str,
    ) -> None:
        ...

    async def validate_user_by_id(
        self,
        user_id: str,
    ) -> User:
        ...
