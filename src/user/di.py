from injector import Binder, Module

from src.user import interfaces
from src.user.services.rental_unit_repository import (
    RentalUnitRepository,
)


class RentalUnitsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.RentalUnitRepository, RentalUnitRepository)  # type: ignore[type-abstract]
