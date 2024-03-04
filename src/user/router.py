from collections.abc import Sequence
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from src.user.schemas import ResponseUserSchema, TokenSchema
from src.user.use_cases import (
    SignUp, Login,
)

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[
    #     Depends(require_organization_access_token),
    # ],
)


@router.post("/signup", description="")
async def signup(
    use_case: Annotated[SignUp, Depends()],
    handler: Annotated[SignUp.Handler, Injected(SignUp.Handler)],
) -> ResponseUserSchema:
    return await handler.execute(use_case)


@router.post("/login", description="Login with email and password ")
async def login(
    use_case: Annotated[Login, Depends()],
    handler: Annotated[Login.Handler, Injected(Login.Handler)],
) -> TokenSchema:
    return await handler.execute(use_case)
