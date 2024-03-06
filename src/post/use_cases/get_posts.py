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
from src.post.schemas import GetPostRequestSchema, PostResponseSchema
from src.settings import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM
from src.user.services.user_repository import UserRepository
from src.user.models import User

import cachetools

# OAuth2 Password Bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/pre/user/login")

# Cache for storing post data for a certain amount of time
cache = cachetools.TTLCache(maxsize=100, ttl=300)  # Cache for 5 minutes


class GetAllPosts(UseCase):
    """
    Use case for getting all posts.
    """

    token: Optional[str] = None

    class Handler(UseCaseHandler["GetAPost", GetPostRequestSchema]):
        """
        Handler for executing the GetAllPosts use case.
        """

        def __init__(
            self,
            post_repository: Inject[PostRepository],
            user_repository: Inject[UserRepository],
        ) -> None:
            """
            Constructor method.

            Args:
                post_repository (PostRepository): Repository for interacting with post data.
                user_repository (UserRepository): Repository for interacting with user data.
            """
            self._post_repository = post_repository
            self._user_repository = user_repository

        async def execute(self, use_case: "GetAllPosts") -> list[PostResponseSchema]:
            """
            Executes the use case to get all posts.

            Args:
                use_case (GetAllPosts): The use case instance.

            Returns:
                list[PostResponseSchema]: List of post response schemas.
            """
            user = await self.verify_token(use_case.token)
            if user:
                return await self.prepare_post_response(email=user.email)

        @cachetools.cached(cache)
        async def prepare_post_response(self, email) -> list[PostResponseSchema]:
            """
            Prepares the post response.

            Args:
                email (str): Email of the user.

            Returns:
                list[PostResponseSchema]: List of post response schemas.
            """
            try:
                posts = await self._post_repository.get_posts_with_user_email(email)
                if len(posts) < 1:
                    raise PostErrors.NO_POSTS_ASSOCIATED
            except IntegrityError as e:
                raise PostErrors.POST_CREATION_ERROR from e

        async def verify_token(self, token: str = Depends(oauth2_scheme)) -> User:
            """
            Verifies the JWT token.

            Args:
                token (str, optional): JWT token. Defaults to Depends(oauth2_scheme).

            Returns:
                User: User object if token is valid.
            """
            try:
                payload = jwt.decode(
                    token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
                )
                email: str = payload.get("email")
                if email is None:
                    raise HTTPException(
                        status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID
                    )
                else:
                    is_valid_email = await self._user_repository.get_token_by_email(
                        email
                    )
                    return is_valid_email
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID
                )
            except jwt.DecodeError:
                raise HTTPException(
                    status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID
                )
