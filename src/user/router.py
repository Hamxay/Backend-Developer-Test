from collections.abc import Sequence
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from src.addresses.schemas import CreateAddressSchema
from src.core.use_cases import UseCase


from src.core.auth import require_organization_access_token
from src.user.schemas import (
    ResponseUserSchema,
    SuccessResponseSchema,
    PermissionEnum,
)
from src.user.use_cases import (
    GetUserList,
    GetUserById,
    CreateUser,
    ModifyUser,
    DeleteUserById,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[
    #     Depends(require_organization_access_token),
    # ],
)


@router.get("", description="Get a list of users")
async def get_user_list(
    use_case: Annotated[GetUserList, Depends()],
    handler: Annotated[GetUserList.Handler, Injected(GetUserList.Handler)],
) -> Sequence[ResponseUserSchema]:
    return await handler.execute(use_case)


@router.get("/{user_id}", description="Get a user by id")
async def get_user_by_id(
    use_case: Annotated[GetUserById, Depends()],
    handler: Annotated[GetUserById.Handler, Injected(GetUserById.Handler)],
) -> ResponseUserSchema:
    return await handler.execute(use_case)


class AnnotatedCreateUser(UseCase):
    first_name: Annotated[str, Body()]
    last_name: Annotated[str, Body()]
    permission: Annotated[PermissionEnum, Body()]
    address: Annotated[Optional[CreateAddressSchema], Body()]


@router.post("", description="Create a user")
async def create_user(
    use_case: Annotated[AnnotatedCreateUser, Body()],
    handler: Annotated[CreateUser.Handler, Injected(CreateUser.Handler)],
) -> ResponseUserSchema:
    use_case_dict = dict(use_case)
    return await handler.execute(CreateUser(**use_case_dict))


class AnnotatedUpdateUser(UseCase):
    first_name: Annotated[Optional[str], Body()]
    last_name: Annotated[Optional[str], Body()]
    permission: Annotated[Optional[PermissionEnum], Body()]
    address: Annotated[Optional[CreateAddressSchema], Body()]


@router.put("/{user_id}", description="Modify a user by id")
async def modify_user(
    user_id: str,
    use_case: Annotated[AnnotatedUpdateUser, Body()],
    handler: Annotated[ModifyUser.Handler, Injected(ModifyUser.Handler)],
) -> ResponseUserSchema:
    use_case_dict = dict(use_case)  # Convert use_case to a dictionary
    return await handler.execute(ModifyUser(user_id=user_id, **use_case_dict))


@router.delete(
    "/{user_id}",
    description="Delete User by Id",
    status_code=200,
    response_model=SuccessResponseSchema,
)
async def delete_user_by_id(
    use_case: Annotated[DeleteUserById, Depends()],
    handler: Annotated[DeleteUserById.Handler, Injected(DeleteUserById.Handler)],
) -> SuccessResponseSchema:
    await handler.execute(use_case)
    return SuccessResponseSchema(status="ok")
