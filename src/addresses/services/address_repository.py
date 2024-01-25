import hashlib
from sqlalchemy import select, delete
from injector import inject

from src.core.unit_of_work import UnitOfWork
from src.addresses.models import Address


class AddressRepository:
    @inject
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def create(self, address: Address) -> str:
        session = await self._unit_of_work.get_db_session()
        sha1_hash = await self.sha1_hash_address(address)

        existing_address = await self.get_address_by_id(sha1_hash)
        if existing_address:
            return existing_address.id  # Return existing address ID if it exists

        address.id = sha1_hash
        session.add(address)
        await session.flush([address])
        return address.id

    async def update(self, address: Address) -> None:
        session = await self._unit_of_work.get_db_session()
        session.add(address)
        await session.flush([address])

    async def delete_by_id(self, address_id: str) -> None:
        session = await self._unit_of_work.get_db_session()
        delete_query = delete(Address).where(Address.id == address_id)
        await session.execute(delete_query)
        await session.commit()

    async def get_address_by_id(self, sha1_hash: str) -> Address | None:
        query = select(Address).where(Address.id == sha1_hash)
        session = await self._unit_of_work.get_db_session()
        result = await session.execute(query)
        return result.scalars().one_or_none()

    async def sha1_hash_address(self, address: Address) -> str:
        street = address.street
        postal_code = address.postal_code
        city = address.city
        state = address.state
        country = address.country
        separator = "|"
        address_string = separator.join([street, postal_code, city, state, country])
        sha1_hash = hashlib.sha1()
        sha1_hash.update(address_string.encode("utf-8"))
        return sha1_hash.hexdigest()
