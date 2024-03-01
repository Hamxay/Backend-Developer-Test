from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_injector import Injected
from jwt import PyJWTError
from src.post.schemas import PostResponseSchema
from src.post.token_auth import get_current_user
from src.post.use_cases import CreateAPost, create_a_post
from src.post.use_cases.delete_a_post import DeleteAPost
from src.post.use_cases.get_posts import GetAllPosts

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/pre/user/signup",
    # scheme_name="JWT"
)

router = APIRouter(
    prefix="/post",
    tags=["posts"],
)
token_auth = None

@router.post("/", description="Create a post")
async def create_a_post(
    use_case: Annotated[CreateAPost, Depends()],
    handler: Annotated[CreateAPost.Handler, Injected(CreateAPost.Handler)],
    # user = Depends(get_current_user)
):
    return await handler.execute(use_case)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all posts",
    # response_model=List[PostResponseSchema],  # Include response model
)
async def get_all_post(
    use_case: Annotated[GetAllPosts, Depends()],
    handler: Annotated[GetAllPosts.Handler, Injected(GetAllPosts.Handler)],
    # token: str = Depends(token_auth.get_current_user),  # Include token verification dependency
):
    return await handler.execute(use_case)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    description="Delete a post",
)
async def delete_a_post(
    use_case: Annotated[DeleteAPost, Depends()],
    handler: Annotated[DeleteAPost.Handler, Injected(DeleteAPost.Handler)],
    # token: str = Depends(token_auth.get_current_user),  # Include token verification dependency
):
    return await handler.execute(use_case)
