from src.user.errors import UserErrors
from src.user.schemas import (
    AddressSchema,
    ResponseUserSchema,
)
from sqlalchemy import Select, select, delete
from sqlalchemy.orm import joinedload
from typing import List, Tuple
from injector import Inject
from src.user import interfaces
from src.user.models import User
from src.core.unit_of_work import UnitOfWork


class UserRepository(interfaces.UserRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def get_by_id(self, user_id: str) -> ResponseUserSchema | None:
        query = self._get_base_query()
        query = query.where(User.id == user_id)

        query = query.options(joinedload(User.address_rel))

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)

        if user := result.scalars().one_or_none():
            address_data = None
            if user.address_rel:
                address_data = AddressSchema.model_validate(user.address_rel)
            return ResponseUserSchema(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                permission=user.permission,
                address=address_data,
            )
        return None

    async def validate_user_by_id(self, user_id: str) -> User:
        query = self._get_base_query().where(User.id == user_id)

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        if user := result.scalars().one_or_none():
            return user
        else:
            raise UserErrors.USER_NOT_FOUND

    async def get_list(self) -> List[ResponseUserSchema]:
        query = self._get_base_query()

        query = query.options(
            joinedload(User.address_rel)  # This adds a join to fetch addresses
        )

        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)

        users = result.scalars().fetchall()

        response_list = []
        for user in users:
            address_data = None
            if user.address_rel:
                address_data = AddressSchema.model_validate(user.address_rel)

            response_list.append(
                ResponseUserSchema(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    permission=user.permission,
                    address=address_data,
                )
            )

        return response_list

    async def create(self, user: User) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(user)
        await session.flush([user])

    async def save(self, user: User) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(user)
        await session.flush([user])

    async def delete_by_id(self, user_id: str) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = delete(User).where(User.id == user_id)
        await session.execute(delete_query)
        await session.commit()

    def _get_base_query(self) -> Select[Tuple[User]]:
        return select(User)
