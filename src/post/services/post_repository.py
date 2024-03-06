from injector import inject
from sqlalchemy import select, delete
from src.core.unit_of_work import UnitOfWork
from src.user.models import User
from src.post.models import Post


class PostRepository:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        """
        Initializes the PostRepository with a UnitOfWork instance.

        Parameters:
        - unit_of_work (UnitOfWork): The unit of work instance to manage database sessions.
        """
        self._unit_of_work = unit_of_work

    async def create(self, post: Post) -> int:
        """
        Creates a new post in the database.

        Parameters:
        - post (Post): The post object to be created.

        Returns:
        - int: The ID of the newly created post.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            post_db = Post(
                id=post.id,
                title=post.title,
                description=post.description,
                created_at=post.created_at,
                created_by_id=post.created_by_id,
            )
            session.add(post_db)
        return post_db.id

    async def get_by_id(self, id: str) -> Post:
        """
        Retrieves a post by its ID from the database.

        Parameters:
        - id (str): The ID of the post to retrieve.

        Returns:
        - Post: The retrieved post object.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(Post).filter(Post.id == id))
            post = result.scalars().first()
        return post

    async def get_posts_with_user_email(self, email):
        """
        Retrieves all posts associated with a user's email address from the database.

        Parameters:
        - email (str): The email address of the user.

        Returns:
        - list[Post]: A list of post objects associated with the user's email address.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            users = await session.execute(select(User).filter(User.email == email))
            user = users.scalars().first()
            result = await session.execute(
                select(Post).filter(Post.created_by_id == user.id)
            )
            posts = result.scalars().all()
        return posts

    async def delete_by_id(self, id: str, user_id: int) -> bool:
        """
        Deletes a post by its ID from the database.

        Parameters:
        - id (str): The ID of the post to delete.
        - user_id (int): The ID of the user who created the post.

        Returns:
        - bool: True if the post was successfully deleted, False otherwise.
        """
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(
                delete(Post).where(Post.id == id, Post.created_by_id == user_id)
            )
            return bool(result.rowcount)
