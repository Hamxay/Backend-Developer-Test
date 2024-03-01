from typing import Protocol, runtime_checkable

from src.user.models import User
from src.user.schemas import ResponseUserSchema


@runtime_checkable
class UserRepository(Protocol):
    async def get_by_id(self, user_id: str) -> ResponseUserSchema | None:
        ...

    async def login_with_email_and_pass(self, email: str, password: str) -> ResponseUserSchema | None:
        ...

    async def create(
        self,
        user: User,
    ) -> None:
        ...
