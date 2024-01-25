from injector import Inject
from sqlalchemy import select

from src.organizations import interfaces
from src.core.unit_of_work import UnitOfWork
from src.organizations.models import Organization


class OrganizationRepository(interfaces.OrganizationRepository):
    def __init__(self, unit_of_work: Inject[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    async def create(self, organization: Organization) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(organization)
        await session.flush([organization])

    async def delete(self, organization_id: int) -> bool:
        session = await self._unit_of_work.get_db_session()
        organization = await session.get(Organization, organization_id)
        if not organization:
            return False

        await session.delete(organization)
        await session.flush([organization])

        return True

    async def get_by_id(self, organization_id: int) -> Organization | None:
        session = await self._unit_of_work.get_db_session()
        query = select(Organization).where(Organization.id == organization_id)
        result = await session.execute(query)
        return result.scalars().one_or_none()
