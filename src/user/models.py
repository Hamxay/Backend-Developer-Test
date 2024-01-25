from typing import Optional
from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from src.core.db.models import Base
from src.user.schemas import PermissionEnum


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(63), primary_key=True)  # noqa: A003
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    permission: Mapped[PermissionEnum] = mapped_column(
        ENUM(PermissionEnum), default=PermissionEnum.IS_OPERATOR
    )
    address: Mapped[Optional[str]] = mapped_column(
        ForeignKey("addresses.id"), nullable=True
    )  # Set nullable to True
    address_rel = relationship("Address")

    __table_args__ = (
        CheckConstraint(
            "id ~* '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$'",
            name="id_format_check",
        ),
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"
