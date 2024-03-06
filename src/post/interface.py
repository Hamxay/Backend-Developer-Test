from typing import Protocol, runtime_checkable, List, Optional
from src.post.models import Post
from src.post.schemas import (
    Post as PostSchema,
    AddPostResponseSchema,
    PostResponseSchema,
)


@runtime_checkable
class PostRepository(Protocol):
    async def delete_by_id(self, post_id: int) -> None:
        """Delete a post by its ID."""
        ...

    async def get_by_id(self, post_id: int) -> PostResponseSchema:
        """Retrieve a post by its ID."""
        ...

    async def create(self, post: PostSchema) -> AddPostResponseSchema:
        """Create a new post."""
        ...

    async def get_posts_with_user_email(self, email):
        """Retrieve all posts by user email."""
        ...
