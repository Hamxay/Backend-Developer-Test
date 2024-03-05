from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from injector import Inject
import jwt
from sqlalchemy.exc import IntegrityError

from src.core.errors import AuthErrors
from src.core.use_cases import UseCase, UseCaseHandler
from src.post.errors import PostErrors
from src.post.services.post_repository import PostRepository
from src.post.schemas import GetPostSChema, PostResponseSchema
from src.settings import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM
from src.user.services.user_repository import UserRepository
from src.user.models import User

import cachetools


class GetAllPosts(UseCase):
    token: Optional[str] = None

    class Handler(UseCaseHandler["GetAPost", GetPostSChema]):
        def __init__(
            self,
            post_repository: Inject[PostRepository],
            user_repository: Inject[UserRepository],
        ) -> None:
            self._post_repository = post_repository
            self._user_repository = user_repository

        async def execute(self, use_case: "GetAllPosts") -> list[PostResponseSchema]:
            is_valid = await self.verify_token(use_case.token)
            print(is_valid.email)
            if is_valid:
                return await self.prepare_post_response(email = is_valid.email)

        cache = cachetools.TTLCache(maxsize=100, ttl=300)  # Cache for 5 minutes

        @cachetools.cached(cache)
        async def prepare_post_response(self, email) -> list[PostResponseSchema]:
            try:
                return await self._post_repository.get_posts_with_user_email(email)
            except IntegrityError as e:
                raise PostErrors.POST_CREATION_ERROR from e

        oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/pre/user/login")

        def verify_token(self, token: str = Depends(oauth2_scheme)) -> User:
            try:
                payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
                email: str = payload.get("email")
                if email is None:
                    raise HTTPException(status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID)
                else:
                    is_valid_email = self._user_repository.get_token_by_email(email)
                    return is_valid_email
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID)
            except jwt.DecodeError:
                raise HTTPException(status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID)
