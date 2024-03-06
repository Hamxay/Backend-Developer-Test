from collections.abc import Sequence
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from src.user.schemas import ResponseUserSchema, TokenSchema
from src.user.use_cases import (
    SignUp,
    Login,
)

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/signup", description="Endpoint to register a new user.")
async def signup(
    use_case: Annotated[SignUp, Depends()],
    handler: Annotated[SignUp.Handler, Injected(SignUp.Handler)],
) -> ResponseUserSchema:
    """
    Create a new user account with the provided user data.

    Args:
        use_case (SignUp): An instance of the SignUp use case containing user data.
        handler (SignUp.Handler): An instance of the SignUp use case handler.

    Returns:
        ResponseUserSchema: The response containing details of the newly created user.

    Raises:
        HTTPException: If an error occurs during user registration.
    """
    return await handler.execute(use_case)


@router.post("/login", description="Endpoint to authenticate and login a user.")
async def login(
    use_case: Annotated[Login, Depends()],
    handler: Annotated[Login.Handler, Injected(Login.Handler)],
) -> TokenSchema:
    """
    Authenticate a user with the provided credentials and generate an access token.

    Args:
        use_case (Login): An instance of the Login use case containing user login credentials.
        handler (Login.Handler): An instance of the Login use case handler.

    Returns:
        TokenSchema: The response containing the JWT access token.

    Raises:
        HTTPException: If login fails due to incorrect credentials or other errors.
    """
    return await handler.execute(use_case)
