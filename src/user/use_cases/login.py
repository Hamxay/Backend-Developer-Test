from _datetime import datetime, timezone, timedelta

from jose import jwt

from src.settings import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM, ACCESS_TOKEN_Time_DELTA
from src.user.errors import UserErrors
from injector import Inject
from src.core.use_cases import UseCase, UseCaseHandler
from src.user.schemas import (
    ResponseUserSchema,
    User as UserSchema,
    UserLoginSchema,
    TokenSchema,
)
from src.user.services.user_repository import (
    UserRepository,
)



class Login(UseCase):
    user: UserLoginSchema

    class Handler(UseCaseHandler["Login", ResponseUserSchema]):
        def __init__(
            self,
            user_repository: Inject[UserRepository],
        ) -> None:
            """
            Initializes the Login use case handler with the user repository dependency.

            :param user_repository: Instance of UserRepository for database interaction.
            """
            self._user_repository = user_repository

        async def execute(self, use_case: "Login") -> TokenSchema:
            """
            Executes the login use case.

            :param use_case: Instance of the Login use case.
            :return: TokenSchema containing the JWT token.
            """
            # Attempt to login with the provided email and password
            user = await self._user_repository.login_with_email_and_pass(
                email=use_case.user.email,
                password=use_case.user.password,
            )
            if not user:
                # If user is not found, raise an error
                raise UserErrors.USER_NOT_FOUND
            # if the previous token is still valid
            payload = jwt.decode(
                user.token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
            )
            token_time = payload.get('exp')
            utc_now = datetime.now(timezone.utc)
            expiration_time_utc = datetime.utcfromtimestamp(token_time).replace(tzinfo=timezone.utc)
            if expiration_time_utc < utc_now:
                # Generate a JWT token for the user
                token = self.generate_token(use_case.user.email)

                # Update the user's token in the database
                await self._user_repository.update_token(user.id, token)
            else:
                token = user.token
            # Prepare and return the response containing the token
            return await self.prepare_user_response(
                use_case.user.email, use_case.user.password, token
            )

        async def prepare_user_response(
            self, email: str, password: str, token: str
        ) -> TokenSchema:
            """
            Prepares the user response with the JWT token.

            :param email: Email of the user.
            :param password: Password of the user.
            :param token: JWT token.
            :return: TokenSchema containing the token.
            """
            # Attempt to login with the provided email and password
            user = await self._user_repository.login_with_email_and_pass(
                email, password
            )
            if not user:
                # If user is not found, raise an error
                raise UserErrors.USER_NOT_FOUND
            token_response = TokenSchema(token=token, token_type="bearer")
            return token_response

        def generate_token(self, email: str) -> str:
            """
            Generates a JWT token for the provided email.

            :param email: Email for which token needs to be generated.
            :return: JWT token.
            """
            # Set the expiration time for the token
            expires_at = datetime.utcnow() + timedelta(hours=1)

            # Create a payload for the token
            payload = {"email": email, "exp": expires_at}

            # Generate the JWT token using the payload and secret key
            token = jwt.encode(payload, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
            return token
