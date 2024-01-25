from sqlalchemy.orm import Mapped, mapped_column
from src.core.db.models import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003

    def __repr__(self) -> str:
        return f"Organization(id={self.id!r})"
