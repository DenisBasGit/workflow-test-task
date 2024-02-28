import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import Base
from src.configs import settings
from src.main import app


engine_test = create_async_engine(settings.TEST_DATABASE_URL_asyncpg, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test
