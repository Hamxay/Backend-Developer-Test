from typing import Protocol, runtime_checkable, List, Optional
from src.post.models import Post
from src.post.schemas import Post as PostSchema


@runtime_checkable
class PostRepository(Protocol):
    async def delete_by_id(self, post_id: int) -> None:
        """Delete a post by its ID."""
        ...

    async def get_by_id(self, post_id: int) -> Optional[PostSchema]:
        """Retrieve a post by its ID."""
        ...

    async def create(self, post: PostSchema) -> None:
        """Create a new post."""
        ...

    async def get_all_posts(self) -> List[PostSchema]:
        """Retrieve all posts."""
        ...
