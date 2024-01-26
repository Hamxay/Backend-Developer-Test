from typing import Optional
from src.addresses.models import Address
from src.addresses.schemas import CreateAddressSchema
from src.addresses.services.address_repository import AddressRepository
from src.core.utils import (
    parse_integrity_error_message,
)
from src.user.models import User
from src.user.schemas import (
    RequestUserSchema,
    ResponseUserSchema,
    PermissionEnum,
)
from injector import Inject
from sqlalchemy.exc import IntegrityError
from src.core.use_cases import UseCase, UseCaseHandler
from src.user.services.user_repository import (
    UserRepository,
)
from src.user.errors import UserErrors


class ModifyUser(UseCase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    permission: Optional[PermissionEnum] = PermissionEnum.IS_OPERATOR
    address: Optional[CreateAddressSchema] = None
    user_id: str

    class Handler(UseCaseHandler["ModifyUser", ResponseUserSchema]):
        def __init__(
            self,
            user_repository: Inject[UserRepository],
            address_repository: Inject[AddressRepository],
        ) -> None:
            self._user_repository = user_repository
            self.address_repository = address_repository

        async def execute(self, use_case: "ModifyUser") -> ResponseUserSchema:
            user = await self._fetch_and_validate_user(use_case.user_id)
            address_id = None  # Default to None if there's no address

            if address := use_case.address:
                # Directly unpack the address attributes into the Address constructor
                address_obj = Address(**address.model_dump())

                # Since we've already checked if address is not None, we can directly create the address
                address_id = await self.address_repository.create(address_obj)

            self._update_user(user, use_case, address_id)
            await self._save_user(user)
            return await self.prepare_user_response(use_case.user_id)

        async def _fetch_and_validate_user(self, user_id: str) -> User:
            user = await self._user_repository.validate_user_by_id(user_id)
            if user is None:
                raise UserErrors.USER_NOT_FOUND
            return user

        def _update_user(
            self,
            user: User,
            use_case: "ModifyUser",
            address_id: Optional[str],
        ) -> None:
            if use_case.first_name is not None:
                user.first_name = use_case.first_name
            if use_case.last_name is not None:
                user.last_name = use_case.last_name
            if use_case.permission is not None:
                user.permission = use_case.permission
            user.address = address_id if address_id else None

        async def _save_user(self, user: User) -> None:
            try:
                await self._user_repository.save(user)
            except IntegrityError as e:
                error_info = str(e)
                error_code = "INTEGRITY_VIOLATION_ERROR"
                keys, values = parse_integrity_error_message(error_info)
                if keys and values:
                    friendly_message = f"Duplicate entry for unique keys {keys} with values {values}. Please provide a unique value."
                else:
                    friendly_message = "An unknown database integrity issue occurred."
                raise UserErrors.dynamic_error(error_code, friendly_message) from e

        async def prepare_user_response(
            self, rental_unit_id: str
        ) -> ResponseUserSchema:
            user = await self._user_repository.get_by_id(rental_unit_id)
            if not user:
                raise UserErrors.USER_NOT_FOUND
            return user
