import datetime
import secrets
import uuid

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from injector import Inject
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.use_cases import UseCase, UseCaseHandler
from src.user.models import User as UserDBModel
from src.user.schemas import ResponseUserSchema, User as UserSchema
from src.user.services.user_repository import UserRepository
from src.user.errors import UserErrors

# Define a secret key for JWT token generation
SECRET_KEY = "your-secret-key"


class SignUp(UseCase):
    user: UserSchema

    class Handler(UseCaseHandler["SignUp", UserSchema]):
        def __init__(
            self, user_repository: Inject[UserRepository],
        ) -> None:
            self._user_repository = user_repository

        async def execute(self, use_case: "SignUp") -> ResponseUserSchema:
            email: str = use_case.user.email
            password: str = use_case.user.password
            user = UserDBModel(
                username=use_case.user.username,
                password=use_case.user.password,
                email=use_case.user.email,
            )
            user_id = await self.create_user(user)

            # Generate JWT token
            token = self.generate_token(use_case.user.email)
            print(token)
            await self._user_repository.update_token(user_id, token)

            return await self.prepare_user_response(email, password, token)

        async def create_user(self, user: UserDBModel) -> int:
            try:
                return await self._user_repository.create(user)
            except IntegrityError as e:
                raise e
                # raise UserErrors.USER_ALREADY_EXISTS from e

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


