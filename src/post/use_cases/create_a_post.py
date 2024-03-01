import uuid
from datetime import timezone, datetime

from injector import Inject
from sqlalchemy.exc import IntegrityError

from src.core.use_cases import UseCase, UseCaseHandler
from src.post.errors import PostErrors
from src.post.services.post_repository import PostRepository
from src.post.schemas import Post, PostResponseSchema
from src.post.models import Post as postDBModel
from src.post.token_auth import verify_token


class CreateAPost(UseCase):
    post: Post

    class Handler(UseCaseHandler["CreateAPost", Post]):
        def __init__(
            self,
            post_repository: Inject[PostRepository],
        ) -> None:
            self._post_repository = post_repository

        async def execute(self, use_case: "CreateAPost") -> PostResponseSchema:
            token = await self._post_repository.get_token_by_user_id(user_id=use_case.post.created_by_id)
            is_valid = verify_token(token)
            if is_valid:
                created_at_str = str(use_case.post.created_at)
                post = postDBModel(
                        title=use_case.post.title,
                        description=use_case.post.description,
                        created_at=created_at_str,
                        created_by_id=use_case.post.created_by_id,
                    )
                post_id = await self.create_post(post)
                return await self.prepare_post_response(post_id)
            else:
                raise "Invalid token"
        # async def _post_exists(self, post_id: int) -> bool:
        #     return await self._post_repository() is not None

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
