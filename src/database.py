from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.configs import settings
from sqlalchemy.orm import Mapped

from src.models import uuid, created_at, updated_at

engine = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

SessionMakerDep = Annotated[AsyncSession, Depends(lambda: async_session_maker)]

async def get_async_session():
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    id: Mapped[uuid]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
