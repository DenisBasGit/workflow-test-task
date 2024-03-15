from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker, get_async_session

SessionMakerDep = Annotated[AsyncSession, Depends(lambda: async_session_maker)]

DatabaseDep = Annotated[AsyncSession, Depends(get_async_session)]
