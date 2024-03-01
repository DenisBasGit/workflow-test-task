from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.repository import GenericSqlRepository
from src.workflow.models import Node

class NodeRepository(GenericSqlRepository[Node]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Node)
