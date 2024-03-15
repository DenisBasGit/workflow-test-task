from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.repository import GenericSqlRepository
from src.workflow.models import Edge


class EdgeRepository(GenericSqlRepository[Edge]):
    """Edge repository"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Edge)
