from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.models import Base
from datetime import datetime


class Post(Base):
    """
    Represents a post in the database.
    """

    __tablename__ = "post"

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(String, default=datetime, nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Define relationships
    created_by = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        """
        Returns a string representation of the Post object.
        """
        return f"Post(id={self.id}, title={self.title}, created_at={self.created_at})"
