from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import Select, and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import exists

from src.database import Base

T = TypeVar("T", bound=Base)


class GenericRepository(Generic[T], ABC):
    """Abstract generic repository"""

    @abstractmethod
    async def get_by_id(self, id_: UUID) -> Optional[T]:
        """
        Get by id

        Args:
            id_(UUID) - indentificator of table
        """
        raise NotImplementedError()

    @abstractmethod
    async def list(self, **filters) -> Sequence[T]:
        """Get list of table"""
        raise NotImplementedError()

    @abstractmethod
    async def add(self, data: Dict[str, Any]) -> T:
        """Add
        Args:
            data(Dict[str, Any]): Record data
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        """Update
        Args:
            record(T): Record data
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, record: T) -> None:
        """Delete
        Args
            id_(UUID): indentificator of table
        """
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):
    """Generic SQL Repository."""

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        """Creates a new repository instance.

        Args:
            session (Session): SQLModel session.
            model_cls (Type[T]): SQLModel class type.
        """
        self._session = session
        self._model_cls = model_cls

    async def _construct_get_stmt(self, id_: UUID) -> Select[tuple[T]]:
        """Creates a SELECT query for retrieving a single record.

        Args:
            id_(UUID):  indentificator of table

        Returns:
            Select: SELECT statement.
        """
        stmt = select(self._model_cls).where(self._model_cls.id == id_)
        return stmt

    async def get_by_id(self, id_: UUID) -> Optional[T]:
        """Get record by id

        Args:
            id_(UUID):  indentificator of table

        Returns:
            Optional[T]: Record
        """
        stmt = await self._construct_get_stmt(id_)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _construct_list_stmt(self, **filters) -> Select[tuple[T]]:
        """Creates a SELECT query for retrieving a multiple records.

        Raises:
            ValueError: Invalid column name.

        Returns:
            Select: SELECT statment.
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

    async def list(self, **filters) -> Sequence[T]:
        """Creates a SELECT query for retrieving a multiple records.

        Returns:
            Sequence[T]: List of records
        """
        stmt = await self._construct_list_stmt(**filters)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def exists(self, **filters) -> bool:
        """Check if record exits by params

        Returns:
            bool: Is object exits or not
        """
        stmt = await self._construct_list_stmt(**filters)
        stmt = exists(stmt).select()
        result = await self._session.execute(stmt)
        return result.scalar()  # type: ignore

    async def add(self, data: Dict[str, Any]) -> T:
        """Add record

        Args:
            data(Dict[str, Any)): Data

        Returns:
            T: Record
        """
        stmt = insert(self._model_cls).values(**data).returning(self._model_cls.id)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def update(self, record: T) -> T:
        """Update record

        Args:
             record(T): Record

        Returns:
            T: Record
        """
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def delete(self, record: T) -> None:
        """
        Delete record

        Args:
            record(T): Record
        """
        await self._session.delete(record)
        await self._session.flush()
