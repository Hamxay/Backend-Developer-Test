from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.db.models import Base
from sqlalchemy.dialects.postgresql import VARCHAR, FLOAT


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[str] = mapped_column(primary_key=True)  # noqa: A003
    street: Mapped[str] = mapped_column(VARCHAR(length=255), nullable=True)
    postal_code: Mapped[str] = mapped_column(VARCHAR(length=10), nullable=True)
    city: Mapped[str] = mapped_column(VARCHAR(length=255), nullable=True)
    state: Mapped[str] = mapped_column(VARCHAR(length=255), nullable=True)
    country: Mapped[str] = mapped_column(VARCHAR(length=2), nullable=True)
    lat: Mapped[float] = mapped_column(FLOAT(asdecimal=True), nullable=True)
    lng: Mapped[float] = mapped_column(FLOAT(asdecimal=True), nullable=True)
    user = relationship("User", back_populates="address_rel")
    __table_args__ = (CheckConstraint("octet_length(id) <= 40", name="id_byte_limit"),)

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}"
