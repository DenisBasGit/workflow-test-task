from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.repository import GenericSqlRepository
from src.workflow.models import Edge, Node


class EdgeRepository(GenericSqlRepository[Edge]):
    """Edge repository"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Edge)

    async def get_by_workflow(self, workflow_id: UUID) -> Sequence[Edge]:
        stmt = select(Edge).where(Edge.from_node.has(Node.workflow_id == workflow_id))
        result = await self._session.execute(stmt)
        return result.scalars().all()
