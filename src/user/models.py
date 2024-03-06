from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.db.models import Base


class User(Base):
    """
    Database model representing a user.

    This class defines the structure of the 'user' table in the database.

    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user.
        email (str): The email address of the user (unique).
        password (str): The password of the user.
        posts (relationship): Relationship with the Post model.
        token (str): JWT token associated with the user.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    posts = relationship("Post", back_populates="created_by")  # Define the relationship
    token = Column(String(255))

    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.

        This method returns a string containing the user's ID, username, and email.

        Returns:
            str: A string representation of the User object.
        """
        return f"User(id={self.id}, username={self.username}, email={self.email})"
