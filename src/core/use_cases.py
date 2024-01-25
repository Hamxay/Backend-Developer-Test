from typing import Protocol, TypeVar

from pydantic import BaseModel


class UseCase(BaseModel):
    pass


UseCaseT = TypeVar("UseCaseT", bound=UseCase, contravariant=True)
ResultT = TypeVar("ResultT", covariant=True)


class UseCaseHandler(Protocol[UseCaseT, ResultT]):
    async def execute(self, use_case: UseCaseT) -> ResultT:
        ...
