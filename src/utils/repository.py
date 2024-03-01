from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, Dict, Any, TypeVar, List

from sqlalchemy import insert, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import exists

from src.database import Base
from src.utils.exceptions import NotFoundException

T = TypeVar("T", bound=Base)

class GenericRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    async def list(self, **filters) -> List[T]:
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):
    """Generic SQL Repository.
    """

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        """Creates a new repository instance.

        Args:
            session (Session): SQLModel session.
            model_cls (Type[T]): SQLModel class type.
        """
        self._session = session
        self._model_cls = model_cls

    async def _construct_get_stmt(self, id: str):
        """Creates a SELECT query for retrieving a single record.

        Args:
            id (str):  Record id.

        Returns:
            SelectOfScalar: SELECT statement.
        """
        stmt = select(self._model_cls).where(self._model_cls.id == id)
        return stmt

    async def get_by_id(self, id: str) -> Optional[T]:
        stmt = await self._construct_get_stmt(id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _construct_list_stmt(self, **filters):
        """Creates a SELECT query for retrieving a multiple records.

        Raises:
            ValueError: Invalid column name.

        Returns:
            SelectOfScalar: SELECT statment.
        """
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    async def list(self, **filters) -> List[T]:
        stmt = await self._construct_list_stmt(**filters)
        result = await self._session.execute(stmt)
        return result.scalars()

    async def exists(self, **filters) -> bool:
        stmt = await self._construct_list_stmt(**filters)
        stmt = exists(stmt).select()
        result = await self._session.execute(stmt)
        return result.scalar()

    async def add(self, data: Dict[str, Any]) -> T:
        stmt = insert(self._model_cls).values(**data).returning(self._model_cls.id)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def update(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def delete(self, record: T) -> None:
        await self._session.delete(record)
        await self._session.flush()
