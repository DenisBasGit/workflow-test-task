from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.repository import GenericSqlRepository
from src.workflow.models import Workflow


class WorkflowRepository(GenericSqlRepository[Workflow]):
    """Workflow Repository"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Workflow)
