from typing import Optional
import uuid
from src.addresses.models import Address
from src.addresses.schemas import CreateAddressSchema
from src.addresses.services.address_repository import AddressRepository
from injector import Inject
from sqlalchemy.exc import IntegrityError

from src.core.use_cases import UseCase, UseCaseHandler
from src.user.models import User
from src.user.schemas import (
    RequestUserSchema,
    ResponseUserSchema,
    PermissionEnum,
)
from src.user.services.user_repository import (
    UserRepository,
)
from src.user.errors import UserErrors


class CreateUser(UseCase):
    first_name: str
    last_name: str
    permission: PermissionEnum
    address: Optional[CreateAddressSchema]

    class Handler(UseCaseHandler["CreateUser", RequestUserSchema]):
        def __init__(
            self,
            user_repository: Inject[UserRepository],
            address_repository: Inject[AddressRepository],
        ) -> None:
            self._user_repository = user_repository
            self.address_repository = address_repository

        async def execute(self, use_case: "CreateUser") -> ResponseUserSchema:
            address = use_case.address
            address_id = None  # Default to None if there's no address

            if address:
                # Directly unpack the address attributes into the Address constructor
                address_obj = Address(**address.model_dump())

                # Since we've already checked if address is not None, we can directly create the address
                address_id = await self.address_repository.create(address_obj)

            user_id = str(uuid.uuid4())

            user = User(
                id=user_id,
                first_name=use_case.first_name,
                last_name=use_case.last_name,
                permission=use_case.permission,
                address=address_id,
            )
            await self.create_user(user)
            return await self.prepare_user_response(user_id)

        async def _user_exists(self, user_id: str) -> bool:
            return await self._user_repository.get_by_id(user_id) is not None

        async def create_user(self, user: User) -> None:
            try:
                await self._user_repository.create(user)
            except IntegrityError as e:
                raise UserErrors.USER_ALREADY_EXISTS from e

        async def prepare_user_response(self, user_id: str) -> ResponseUserSchema:
            user = await self._user_repository.get_by_id(user_id)
            if not user:
                raise UserErrors.USER_NOT_FOUND
            return user
