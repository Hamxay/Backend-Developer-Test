from typing import Annotated

from cachetools import TTLCache
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi_injector import Injected
from starlette.responses import JSONResponse

from src.core.auth import require_valid_access_token
from src.post.schemas import AddPostResponseSchema, PostResponseSchema
from src.post.use_cases.create_a_post import CreateAPost
from src.post.use_cases.delete_a_post import DeleteAPost
from src.post.use_cases.get_posts import GetAllPosts
cache = TTLCache(maxsize=1000, ttl=300)

router = APIRouter(
    prefix="/post",
    tags=["posts"],
    dependencies=[
        Depends(require_valid_access_token)]
)


async def get_access_token(request: Request):
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    try:
        token_type, token = authorization.split()
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return token
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")


@router.post("/", description="Create a post", response_model=AddPostResponseSchema)
async def create_a_post(
    use_case: Annotated[CreateAPost, Depends()],
    handler: Annotated[CreateAPost.Handler, Injected(CreateAPost.Handler)],
    request: Request,
) -> AddPostResponseSchema:
    total_size = len(use_case.json())
    if total_size > 1024 * 1024:
        raise HTTPException(status_code=413, detail="Payload size exceeds 1 MB")
    token = await get_access_token(request)
    use_case.token = token
    post_id = await handler.execute(use_case)
    return AddPostResponseSchema(post_id=post_id)


@router.get("/", description="Get all posts"
    # , response_model=list[PostResponseSchema]
            )
async def get_all_post(
    use_case: Annotated[GetAllPosts, Depends()],
    handler: Annotated[GetAllPosts.Handler, Injected(GetAllPosts.Handler)],
    request: Request
):
    url_key = str(request.headers.get('authorization'))
    cached_data = cache.get(url_key)
    if cached_data:
        return cached_data  # Return cached data directly
    token = await get_access_token(request)
    use_case.token = token
    response_data = await handler.execute(use_case)
    cache[url_key] = url_key
    return response_data


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    description="Delete a post",
)
async def delete_a_post(
    use_case: Annotated[DeleteAPost, Depends()],
    handler: Annotated[DeleteAPost.Handler, Injected(DeleteAPost.Handler)],
):
    return await handler.execute(use_case)
