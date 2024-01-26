from src.addresses.services.address_repository import AddressRepository
from src.user.errors import UserErrors
from injector import Inject
from src.core.use_cases import UseCase, UseCaseHandler
from src.user.schemas import (
    ResponseUserSchema,
)
from src.user.services.user_repository import (
    UserRepository,
)


class GetUserById(UseCase):
    user_id: str

    class Handler(UseCaseHandler["GetUserById", ResponseUserSchema]):
        def __init__(
            self,
            rental_unit_repository: Inject[UserRepository],
            address_repository: Inject[AddressRepository],
        ) -> None:
            self.rental_unit_repository = rental_unit_repository
            self.address_repository = address_repository

        async def execute(self, use_case: "GetUserById") -> ResponseUserSchema:
            user = await self.rental_unit_repository.get_by_id(
                use_case.user_id,
            )
            if not user:
                raise UserErrors.USER_NOT_FOUND

            return user
