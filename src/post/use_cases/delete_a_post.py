from injector import Inject
from sqlalchemy.exc import IntegrityError
from src.core.use_cases import UseCase, UseCaseHandler
from src.post.errors import PostErrors
from src.post.services.post_repository import PostRepository
from src.post.schemas import GetPostSChema


class DeleteAPost(UseCase):
    id: str

    class Handler(UseCaseHandler["DeleteAPost", GetPostSChema]):
        def __init__(
            self,
            post_repository: Inject[PostRepository],
        ) -> None:
            self._post_repository = post_repository

        async def execute(self, use_case: "DeleteAPost"):
            return await self.delete_by_id(use_case.id)

        async def delete_by_id(self, id: str):
            try:
                await self._post_repository.delete_by_id(id)
                if await self._post_repository.get_by_id(id) is None:
                    return "Post deleted successfully"
            except IntegrityError as e:
                raise PostErrors.POST_NOT_FOUND from e

