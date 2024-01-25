from injector import Binder, Module

from src.organizations import interfaces
from src.organizations.services.organization_repository import (
    OrganizationRepository,
)


class OrganizationModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.OrganizationRepository, OrganizationRepository)  # type: ignore[type-abstract]
