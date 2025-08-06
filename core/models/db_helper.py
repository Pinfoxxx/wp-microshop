# ====== Database helper for working with SQLite ====== #


from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from core.config import settings


class DatabaseHelper:

    # Creating method which activate session factory
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Creating async session factory
        self.session_factory = async_sessionmaker(
            bind=self.engine,  # Engine param
            autoflush=False,  # Falsed autoreset
            autocommit=False,  # Falsed autocommit
            expire_on_commit=False,  # Falsed expiring on commit
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    # Method for work with new session
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as conn:
            yield conn
            await conn.close()

    # Method for work with scoped session
    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.DB.URL,
    echo=settings.DB.ECHO,
)
