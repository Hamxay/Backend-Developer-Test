from injector import inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.unit_of_work import UnitOfWork
from src.user.models import User


class UserRepository:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def create(self, user: User) -> int:
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            user_db = User(
                username=user.username,
                email=user.email,
                password=user.password
            )
            session.add(user_db)
        return user_db.id

    async def get_by_id(self, id: int) -> User:
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.id == id))
            user = result.scalars().first()
        return user

    async def get_by_email(self, email: str) -> User:
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.email == email))
            user = result.scalars().first()
        return user

    async def login_with_email_and_pass(self, email, password):
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.email == email, User.password == password))
            user = result.scalars().first()
        return user

    async def update_token(self, user_id: int, token: str) -> None:
        """
        Update the JWT token associated with the user in the database.
        :param user_id: ID of the user whose token needs to be updated
        :param token: New JWT token to be updated
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                user.token = token
                session.add(user)

    async def get_token_by_email(self, email) -> User:
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.email == email))
            user = result.scalars().first()
        return user
