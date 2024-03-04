from typing import Optional

from cachetools import TTLCache

from src.core.errors import AuthErrors
from src.settings import (
    ACCESS_TOKEN_ALGORITHM,
    ACCESS_TOKEN_SECRET_KEY,
)

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from injector import Inject
import jwt
from sqlalchemy.exc import IntegrityError

from src.core.use_cases import UseCase, UseCaseHandler
from src.post.errors import PostErrors
from src.post.services.post_repository import PostRepository
from src.post.schemas import Post, PostResponseSchema
from src.post.models import Post as postDBModel
from src.user.models import User
from src.user.services.user_repository import UserRepository

cache = TTLCache(maxsize=100, ttl=300)


class CreateAPost(UseCase):
    post: Post
    token: Optional[str] = None

    class Handler(UseCaseHandler["CreateAPost", Post]):
        def __init__(
            self,
            post_repository: Inject[PostRepository],
            user_repository: Inject[UserRepository],
        ) -> None:
            self._post_repository = post_repository
            self._user_repository = user_repository

        async def execute(
            self,
            use_case: "CreateAPost",

        ) -> PostResponseSchema:
            is_valid = await self.verify_token(use_case.token)
            if is_valid:
                created_at_str = str(use_case.post.created_at)
                post = postDBModel(
                        title=use_case.post.title,
                        description=use_case.post.description,
                        created_at=created_at_str,
                        created_by_id=is_valid.id,
                    )
                post_id = await self.create_post(post)
                response = await self.prepare_post_response(post_id)
                cache[use_case.token] = response

                return response

        async def create_post(self, post: postDBModel) -> int:
            try:
                return await self._post_repository.create(post)
            except IntegrityError as e:
                raise PostErrors.POST_ALREADY_EXISTS from e

        async def prepare_post_response(self, post_id) -> PostResponseSchema:
            post = await self._post_repository.get_by_id(post_id)
            if not post:
                raise PostErrors.POST_NOT_FOUND
            return post

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
