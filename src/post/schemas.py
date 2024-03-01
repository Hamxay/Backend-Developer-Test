from datetime import datetime, timezone

from pydantic import BaseModel

from src.user.schemas import UserRelation


class Post(BaseModel):
    title: str
    description: str
    created_at: datetime
    created_by_id: int


class PostResponseSchema:
    description: str
    title: str
    created_by_id: int


class GetPostSChema(BaseModel):
    id: int
