from fastapi import Depends
from src.database import get_async_session
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

DatabaseDep = Annotated[AsyncSession, Depends(get_async_session)]