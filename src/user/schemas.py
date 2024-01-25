from src.addresses.schemas import AddressSchema
from pydantic import BaseModel
from enum import Enum


class PermissionEnum(str, Enum):
    IS_ADMIN = "IS_ADMIN"
    IS_MANAGER = "IS_MANAGER"
    IS_OPERATOR = "IS_OPERATOR"


class RequestUserSchema(BaseModel):
    first_name: str
    last_name: str
    address: AddressSchema | None
    permission: PermissionEnum = PermissionEnum.IS_OPERATOR

    class Config:
        from_attributes = True


class ResponseUserSchema(RequestUserSchema):
    id: str  # noqa: A003

    class Config:
        from_attributes = True


class SuccessResponseSchema(BaseModel):
    status: str
