import asyncio
from typing import Any, AsyncIterable, Iterator

import pytest
from factory.alchemy import SQLAlchemyModelFactory
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session

from src.configs import settings
from src.database import Base, async_session_maker, sync_session_maker
from src.main import app
from tests.test_types import DBInsert

pytest_plugins = [
    "tests.workflow.factories.workflow",
]

test_session = scoped_session(sync_session_maker())


def get_event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_sessionstart(session: Any) -> None:
    async def init_db() -> None:
        engine = create_async_engine(settings.DATABASE_URL_asyncpg)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    for loop in get_event_loop():
        loop.run_until_complete(init_db())


def pytest_sessionfinish(session: Any, exitstatus: Any) -> None:
    async def close_db() -> None:
        engine = create_async_engine(settings.DATABASE_URL_asyncpg)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    for loop in get_event_loop():
        loop.run_until_complete(close_db())


# @pytest.fixture
# async def db_session(async_session):
#     async with async_session() as session:
#         yield session


@pytest.fixture
async def db() -> AsyncIterable[AsyncSession]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def db_ins(db: AsyncSession) -> AsyncIterable[DBInsert]:
    async def insert(factory: SQLAlchemyModelFactory, **kwargs: Any) -> Any:
        instance = factory.build(**kwargs)
        db.add(instance)
        await db.commit()
        return instance

    yield insert


@pytest.fixture(scope="session")
async def db_session() -> AsyncIterable[AsyncSession]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def db_session_commit(db_session: AsyncSession) -> None:
    await db_session.commit()


@pytest.fixture(scope="session")
async def client() -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c
