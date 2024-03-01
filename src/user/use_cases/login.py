import datetime

from jose import jwt

from src.user.errors import UserErrors
from injector import Inject
from src.core.use_cases import UseCase, UseCaseHandler
from src.user.schemas import (
    ResponseUserSchema,
    User as UserSchema, UserLoginSchema
)
from src.user.services.user_repository import (
    UserRepository,
)
SECRET_KEY = "your-secret-key"


class Login(UseCase):
    user: UserLoginSchema

    class Handler(UseCaseHandler["Login", ResponseUserSchema]):
        def __init__(
            self,
            user_repository: Inject[UserRepository],
        ) -> None:
            self._user_repository = user_repository

        async def execute(self, use_case: "Login") -> ResponseUserSchema:
            user = await self._user_repository.login_with_email_and_pass(
                email=use_case.user.email,
                password=use_case.user.password,
            )
            if not user:
                raise UserErrors.USER_NOT_FOUND
            user_id = user.id

            token = self.generate_token(use_case.user.email)
            await self._user_repository.update_token(user_id, token)

            return await self.prepare_user_response(use_case.user.email, use_case.user.password, token)

        async def prepare_user_response(
            self, email: str, password: str, token: str
        ) -> ResponseUserSchema:
            user = await self._user_repository.login_with_email_and_pass(email, password)
            if not user:
                raise UserErrors.USER_NOT_FOUND
            return user

        def generate_token(self, email: str) -> str:
            # Set the expiration time for the token
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            payload = {"email": email, "exp": expires_at}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return token
