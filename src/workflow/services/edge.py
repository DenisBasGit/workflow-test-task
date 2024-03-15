from typing import Any, Dict, Sequence, Type
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.workflow.constants import NodeType
from src.workflow.models import Edge
from src.workflow.repositories import EdgeRepository
from src.workflow.schemas import CreateEdgeSchema
from src.workflow.services.exceptions import EdgeNotExists, UnableCreateEdgeExeption

from .node import NodeService


class EdgeService:
    """Edge service"""

    def __init__(self, session: AsyncSession, repository: Type[EdgeRepository]):
        self.session = session
        self.repository = repository(self.session)  # noqa
        self.node_service = NodeService(self.session)

    async def list(self, **filters) -> Sequence[Edge]:
        """
        Get list of record

        Args:
            **filters(Dict[str, str]) -> Key is column of table and value is value. Example: id=1
        Return:
            ScalarResult(T) -> List of record
        """
        return await self.repository.list(**filters)

    async def create(self, data: CreateEdgeSchema) -> Edge:
        """
        Create Record
        Args:
            data(CreateEdgeSchema) -> Data for create record
        Return:
            Edge: New Record
        """
        validated_data = await self.validate(data)
        try:
            edge = await self.repository.add(validated_data)
        except IntegrityError:
            raise UnableCreateEdgeExeption()
        await self.session.commit()
        return edge

    async def validate(self, data: CreateEdgeSchema) -> Dict[str, Any]:
        """
        Validate
        Args:
            data(CreateEdgeSchema) -> Data for create record
        Return:
            validated_data(Dict[str, Any]) -> Validated data
        """
        validate_data = data.model_dump()
        from_node = await self.node_service.get_or_except(
            validate_data["from_node_id"], exception=UnableCreateEdgeExeption
        )
        to_node = await self.node_service.get_or_except(validate_data["to_node_id"], exception=UnableCreateEdgeExeption)
        if from_node.workflow_id != to_node.workflow_id:
            raise UnableCreateEdgeExeption("Cannot create edge between nodes with other workflow.")
        if from_node.type == NodeType.END:
            raise UnableCreateEdgeExeption("Edge cannot be create. Start node cannot have incoming relation")
        if to_node.type == NodeType.START:
            raise UnableCreateEdgeExeption("Edge cannot be create. End node cannot have incoming relation")
        if from_node.type == NodeType.MESSAGE and await from_node.edges_from_count >= 1:
            raise UnableCreateEdgeExeption("Message node cannot have more than 1 output.")
        if to_node.type == NodeType.CONDITION and from_node.type not in (NodeType.MESSAGE, NodeType.CONDITION):
            raise UnableCreateEdgeExeption("Condition node can related only with Message and condition node.")
        if from_node.type == NodeType.CONDITION and await from_node.edges_from_count >= 2:
            raise UnableCreateEdgeExeption("Node condition can have only 2 output edges.")
        return validate_data

    async def delete(self, id_: UUID) -> None:
        """
        Delete Record from database
        Args:
            id_: Indentificator of table
        Exception:
            EdgeNotExists - when record not found
        """
        record = await self.repository.get_by_id(id_)
        if record is None:
            raise EdgeNotExists()
        await self.repository.delete(record)
        await self.session.commit()

    async def exists(self, **filters) -> bool:
        """
        Check if record exists in database
        Args:
            **filters(Dict[str, str]): Key is column of table and value is value. Example: id=1
        Return:
            bool: Is object exists
        """
        return await self.repository.exists(**filters)
