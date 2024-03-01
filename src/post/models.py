from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db.models import Base
from src.user.models import User
from datetime import datetime


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(String, default=datetime, nullable=False)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Define relationships
    created_by = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title}, created_at={self.created_at})"
