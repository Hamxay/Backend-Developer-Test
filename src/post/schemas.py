from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    """
    Pydantic model representing a post.
    """
    title: str  # Title of the post
    description: str  # Description of the post
    created_at: datetime  # Timestamp indicating when the post was created


class PostResponseSchema(BaseModel):
    """
    Pydantic model representing the response for a post.
    """
    id: str  # Unique identifier for the post
    description: str  # Description of the post
    title: str  # Title of the post
    created_by_id: int  # ID of the user who created the post
    created_at: datetime  # Timestamp indicating when the post was created


class GetPostRequestSchema(BaseModel):
    """
    Pydantic model representing the request to get a post.
    """
    id: int  # ID of the post to retrieve


class AddPostResponseSchema(BaseModel):
    """
    Pydantic model representing the response after adding a post.
    """
    post_id: str  # ID of the newly added post


class DeletePostRequestSchema(BaseModel):
    """
    Pydantic model representing the request to delete a post.
    """
    id: str  # ID of the post to delete


class DeletePostResponse(BaseModel):
    """
    Pydantic model representing the response after deleting a post.
    """
    success: str  # Indicates the success message after deleting the post
