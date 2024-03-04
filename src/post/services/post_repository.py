from injector import inject
from sqlalchemy import select, delete
from src.core.unit_of_work import UnitOfWork
from src.user.models import User
from src.post.models import Post


class PostRepository:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def create(self, post: Post) -> int:
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            post_db = Post(
                title=post.title,
                description=post.description,
                created_at=post.created_at,
                created_by_id=post.created_by_id
            )
            session.add(post_db)
        return post_db.id

    async def get_by_id(self, id: int) -> Post:
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(Post).filter(Post.id == id))
            post = result.scalars().first()
        return post

    async def get_all(self):
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            result = await session.execute(select(Post))
            posts = result.scalars().all()
        return posts

    async def delete_by_id(self, id: int):
        session = await self._unit_of_work.get_db_session()
        async with session.begin():
            await session.execute(delete(Post).where(Post.id == id))


