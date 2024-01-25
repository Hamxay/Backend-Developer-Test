from typing import Annotated, Generic, Literal, TypeVar, Sequence
from pydantic import BaseModel, StringConstraints, ConfigDict

EntityT = TypeVar("EntityT")


class ErrorDetail(BaseModel):
    field: str | None
    issue: str
    location: Literal["body", "path", "query"]


class Error(BaseModel):
    name: Annotated[str, Annotated[str, StringConstraints(to_upper=True)]]
    message: str
    details: Sequence[ErrorDetail] | None = None


class PaginatedResult(BaseModel, Generic[EntityT]):
    page_number: int
    total_results: int
    results: Sequence[EntityT]
    model_config = ConfigDict(arbitrary_types_allowed=True)
