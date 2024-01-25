from typing import Protocol, runtime_checkable

from src.organizations.models import Organization


@runtime_checkable
class OrganizationRepository(Protocol):
    async def create(
        self,
        organization: Organization,
    ) -> None:
        ...

    async def delete(
        self,
        organization_id: int,
    ) -> bool:
        ...

    async def get_by_id(
        self,
        organization_id: int,
    ) -> Organization | None:
        ...
