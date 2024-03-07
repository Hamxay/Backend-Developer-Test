from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from injector import Inject
from sqlalchemy.exc import IntegrityError

from src.core.errors import AuthErrors
from src.user.models import User

from src.core.use_cases import UseCase, UseCaseHandler
from src.post.errors import PostErrors
from src.post.services.post_repository import PostRepository
from src.post.schemas import DeletePostRequestSchema, DeletePostResponse
from src.settings import (
    ACCESS_TOKEN_SECRET_KEY,
    ACCESS_TOKEN_ALGORITHM,
    OAUTH_TOKEN_URL,
)
from src.user.services.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAUTH_TOKEN_URL)


class DeleteAPost(UseCase):
    """Use case to delete a post."""

    post: DeletePostRequestSchema
    token: Optional[str] = Depends(oauth2_scheme)

    class Handler(UseCaseHandler["DeleteAPost", DeletePostRequestSchema]):
        """Handler for the delete post use case."""

        def __init__(
            self,
            post_repository: Inject[PostRepository],
            user_repository: Inject[UserRepository],
        ) -> None:
            self._post_repository = post_repository
            self._user_repository = user_repository

        async def execute(self, use_case: "DeleteAPost"):
            """Execute the use case to delete a post.

            Args:
            - use_case: The use case instance containing the post ID to delete.
            """
            user = await self.verify_token(use_case.token)
            if user:
                return await self.delete_by_id(use_case.post.id, user.id)

        async def delete_by_id(self, id: str, user_id: int) -> DeletePostResponse:
            """Delete a post by its ID.

            Args:
            - id: The ID of the post to delete.

            Returns:
            - str: A message indicating the result of the deletion operation.
            """
            try:
                # Attempt to delete the post by its ID
                is_deleted = await self._post_repository.delete_by_id(id, user_id)
                # Check if the post was successfully deleted
                if await self._post_repository.get_by_id(id) is None and is_deleted:
                    return DeletePostResponse(success="Post Deleted Successfully")
                else:
                    raise PostErrors.POST_NOT_FOUND
            except IntegrityError as e:
                # If the post is not found, raise an error
                raise PostErrors.POST_NOT_FOUND from e

        async def verify_token(self, token: str = Depends(oauth2_scheme)) -> User:
            """Verify the access token.

            Args:
            - token: The access token to be verified.

            Returns:
            - User: The user associated with the token if valid.
            """
            try:
                # Decode the access token
                payload = jwt.decode(
                    token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
                )
                email: str = payload.get("email")
                if email is None:
                    # If email not found in token, raise error
                    raise HTTPException(
                        status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID
                    )
                else:
                    return await self._user_repository.get_token_by_email(email)
            except jwt.ExpiredSignatureError:
                # If token has expired, raise error
                raise HTTPException(
                    status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID
                )
            except jwt.DecodeError:
                # If token decoding fails, raise error
                raise HTTPException(
                    status_code=401, detail=AuthErrors.ACCESS_TOKEN_INVALID
                )
