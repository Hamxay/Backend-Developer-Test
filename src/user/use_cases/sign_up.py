import datetime
import jwt
from injector import Inject
from sqlalchemy.exc import IntegrityError

from src.core.use_cases import UseCase, UseCaseHandler
from src.settings import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM, ACCESS_TOKEN_Time_DELTA
from src.user.models import User as UserDBModel
from src.user.schemas import ResponseUserSchema, User as UserSchema
from src.user.services.user_repository import UserRepository
from src.user.errors import UserErrors


class SignUp(UseCase):
    user: UserSchema

    class Handler(UseCaseHandler["SignUp", UserSchema]):
        def __init__(
            self,
            user_repository: Inject[UserRepository],
        ) -> None:
            """
            Initializes the SignUp use case handler with the user repository dependency.

            :param user_repository: Instance of UserRepository for database interaction.
            """
            self._user_repository = user_repository

        async def execute(self, use_case: "SignUp") -> ResponseUserSchema:
            """
            Executes the sign-up use case.

            :param use_case: Instance of the SignUp use case.
            :return: ResponseUserSchema containing user details.
            """
            email: str = use_case.user.email
            password: str = use_case.user.password

            # Create a UserDBModel instance from the provided user schema
            user = UserDBModel(
                username=use_case.user.username,
                password=use_case.user.password,
                email=use_case.user.email,
            )

            # Attempt to create the user in the database
            user_id = await self.create_user(user)

            # Generate a JWT token for the user
            token = self.generate_token(use_case.user.email)

            # Update the user's token in the database
            await self._user_repository.update_token(user_id, token)

            # Prepare and return the response containing the user details
            return await self.prepare_user_response(email, password)

        async def create_user(self, user: UserDBModel) -> int:
            """
            Creates a new user in the database.

            :param user: UserDBModel instance representing the user to be created.
            :return: ID of the created user.
            """
            try:
                return await self._user_repository.create(user)
            except IntegrityError as e:
                raise e

        async def prepare_user_response(
            self,
            email: str,
            password: str,
        ) -> ResponseUserSchema:
            """
            Prepares the user response with the user details.

            :param email: Email of the user.
            :param password: Password of the user.
            :return: ResponseUserSchema containing user details.
            """
            # Attempt to retrieve the user from the database using email and password
            user = await self._user_repository.login_with_email_and_pass(
                email, password
            )
            if not user:
                # If user is not found, raise an error
                raise UserErrors.USER_NOT_FOUND
            return user

        def generate_token(self, email: str) -> str:
            """
            Generates a JWT token for the provided email.

            :param email: Email for which token needs to be generated.
            :return: JWT token.
            """
            # Set the expiration time for the token
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

            # Create a payload for the token
            payload = {"email": email, "exp": expires_at}

            # Generate the JWT token using the payload and secret key
            token = jwt.encode(payload, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
            return token
