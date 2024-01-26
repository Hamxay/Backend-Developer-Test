from injector import Inject
from src.core.use_cases import UseCase, UseCaseHandler
from src.user.errors import UserErrors
from src.user.services.user_repository import (
    UserRepository,
)


class DeleteUserById(UseCase):
    user_id: str

    class Handler(UseCaseHandler["DeleteUserById", None]):
        def __init__(self, user_repository: Inject[UserRepository]) -> None:
            self.user_repository = user_repository

        async def execute(self, use_case: "DeleteUserById") -> None:
            user = await self.user_repository.get_by_id(
                use_case.user_id,
            )
            if not user:
                raise UserErrors.USER_NOT_FOUND

            await self.user_repository.delete_by_id(
                use_case.user_id,
            )
