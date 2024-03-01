from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.db.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    posts = relationship("Post", back_populates="created_by")  # Define the relationship
    token = Column(String(255))
    # Define relationships if necessary
    # posts = relationship("Post", back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"
