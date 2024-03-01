import uuid
from datetime import timezone, datetime

from injector import Inject
from sqlalchemy.exc import IntegrityError

from src.core.use_cases import UseCase, UseCaseHandler
from src.post.errors import PostErrors
from src.post.services.post_repository import PostRepository
from src.post.schemas import GetPostSChema, PostResponseSchema
from src.post.models import Post as postDBModel


class GetAllPosts(UseCase):
    class Handler(UseCaseHandler["GetAPost", GetPostSChema]):
        def __init__(
            self,
            post_repository: Inject[PostRepository],
        ) -> None:
            self._post_repository = post_repository

        async def execute(self, use_case: "GetAllPosts") -> list[PostResponseSchema]:
            return await self.get_posts()
            # return await self.prepare_post_response(use_case.post.id)

        # async def _post_exists(self, post_id: int) -> bool:
        #     return await self._post_repository() is not None

        async def get_posts(self):
            try:
                return await self._post_repository.get_all()
            except IntegrityError as e:
                raise PostErrors.POST_NOT_FOUND from e

        # async def prepare_post_response(self, post_id) -> PostResponseSchema:
        #     post = await self._post_repository.get_by_id(post_id)
        #     if not post:
        #         raise PostErrors.POST_NOT_FOUND
        #     return post
