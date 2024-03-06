from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    title:  str
    description:  str
    created_at: datetime


class PostResponseSchema(BaseModel):
    id: str
    description: str
    title: str
    created_by_id: int
    created_at: datetime


class GetPostRequestSchema(BaseModel):
    id: int


class AddPostResponseSchema(BaseModel):
    post_id: str


class DeletePostRequestSchema(BaseModel):
    id: str


class DeletePostResponse(BaseModel):
    success: str
