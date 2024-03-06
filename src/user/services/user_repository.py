from injector import inject
from sqlalchemy import select
from src.core.unit_of_work import UnitOfWork
from src.user.models import User


class UserRepository:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        """
        Initializes the UserRepository with the provided unit of work.

        :param unit_of_work: Unit of work for interacting with the database.
        """
        self._unit_of_work = unit_of_work

    async def create(self, user: User) -> int:
        """
        Create a new user in the database.

        :param user: User object containing user details.
        :return: ID of the newly created user.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            user_db = User(
                username=user.username, email=user.email, password=user.password
            )
            session.add(user_db)
        return user_db.id

    async def get_by_id(self, id: int) -> User:
        """
        Retrieve a user from the database by its ID.

        :param id: ID of the user to retrieve.
        :return: User object if found, None otherwise.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.id == id))
            user = result.scalars().first()
        return user

    async def get_by_email(self, email: str) -> User:
        """
        Retrieve a user from the database by its email address.

        :param email: Email address of the user to retrieve.
        :return: User object if found, None otherwise.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.email == email))
            user = result.scalars().first()
        return user

    async def login_with_email_and_pass(self, email, password):
        """
        Perform user login with email and password.

        :param email: Email address of the user.
        :param password: Password of the user.
        :return: User object if login is successful, None otherwise.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(
                select(User).filter(User.email == email, User.password == password)
            )
            user = result.scalars().first()
        return user

    async def update_token(self, user_id: int, token: str) -> None:
        """
        Update the JWT token associated with the user in the database.

        :param user_id: ID of the user whose token needs to be updated.
        :param token: New JWT token to be updated.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                user.token = token
                session.add(user)

    async def get_token_by_email(self, email) -> User:
        """
        Retrieve a user's token from the database by its email address.

        :param email: Email address of the user.
        :return: User object if found, None otherwise.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(User).filter(User.email == email))
            user = result.scalars().first()
        return user
