from injector import Inject
from src.core.use_cases import UseCase, UseCaseHandler
from src.user.schemas import (
    ResponseUserSchema,
)
from src.user.services.user_repository import (
    UserRepository,
)
from typing import List


class GetUserList(UseCase):
    class Handler(UseCaseHandler["GetUserList", List[ResponseUserSchema]]):
        def __init__(
            self,
            user_repository: Inject[UserRepository],
        ) -> None:
            self.user_repository = user_repository

        async def execute(self, use_case: "GetUserList") -> List[ResponseUserSchema]:
            return await self.user_repository.get_list()
