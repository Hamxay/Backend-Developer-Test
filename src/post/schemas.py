from datetime import datetime, timezone

from pydantic import BaseModel, constr

from src.user.schemas import UserRelation


class Post(BaseModel):
    title:  str
    description:  str
    created_at: datetime
    # created_by_id: int


class PostResponseSchema:
    post_id = str
    description: str
    title: str
    created_by_id: int


class GetPostSChema(BaseModel):
    id: int


class AddPostResponseSchema(BaseModel):
    post_id: str
