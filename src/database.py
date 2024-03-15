from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker

from src.configs import settings
from src.models import created_at, updated_at, uuid

engine = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

sync_engine = create_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

sync_session_maker = sessionmaker(sync_engine, expire_on_commit=False)


async def get_async_session():
    """Get async session"""
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    """Base class for models"""

    id: Mapped[uuid]  # type: ignore
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 3
    repr_cols: Tuple[str, ...] = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
