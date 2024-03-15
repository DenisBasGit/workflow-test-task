from typing import Any, Callable, Dict, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import WRKFEception
from src.workflow.constants import NodeType
from src.workflow.models import Node
from src.workflow.repositories import NodeRepository
from src.workflow.schemas import CreateNodeSchema
from src.workflow.services.exceptions import NodeNotExists, UnableCreateNodeException

from .workflow import WorkflowService


class NodeService:
    """Node service"""

    def __init__(self, session: AsyncSession, repository: Callable[[AsyncSession], NodeRepository] | None = None):
        self.session = session
        if repository is None:
            repository = NodeRepository
        self.repository = repository(self.session)

    async def list(self, **filters) -> Sequence[Node]:
        """
        Get list of record

        Args:
            **filters(Dict[str, str]) -> Key is column of table and value is value. Example: id=1
        Return:
            ScalarResult(Node) -> List of record
        """
        return await self.repository.list(**filters)

    async def create(self, data: CreateNodeSchema) -> Node:
        """
        Create Record
        Args:
            data(CreateNodeSchema) -> Data for create record
        Return:
            Node: New Record
        """
        validated_data = await self.validate(data)
        node = await self.repository.add(validated_data)
        await self.session.commit()
        return node

    async def delete(self, id_: UUID) -> None:
        """
        Delete Record from database
        Args:
            id_: Indentificator of table
        Raise:
            NodeNotExists - when record not found
        """
        record = await self.repository.get_by_id(id_)
        if record is None:
            raise NodeNotExists()
        await self.repository.delete(record)
        await self.session.commit()

    async def validate(self, data: CreateNodeSchema) -> Dict[str, Any]:
        """
        Validate
        Args:
            data(CreateEdgeSchema) -> Data for create record
        Return:
            validated_data(Dict[str, Any]) -> Validated data
        """
        validate_data = data.model_dump()
        workflow_service = WorkflowService(self.session)
        is_workflow_exists = await workflow_service.exists(id=validate_data["workflow_id"])
        if not is_workflow_exists:
            raise UnableCreateNodeException(f"Workflow {validate_data['workflow_id']} not exists")
        if validate_data["type"] in (NodeType.START, NodeType.END):
            del validate_data["text"]
            del validate_data["status"]
            is_node_exists = await self.exists(type=validate_data["type"], workflow_id=validate_data["workflow_id"])
            print("Is Node exists: ", is_node_exists)
            if is_node_exists:
                raise UnableCreateNodeException("Workflow cannot have more than 1 'start' and 'end' node")
        return validate_data

    async def get_or_except(self, id_: UUID, exception: type[WRKFEception] | None = None) -> Node:
        """
        Get or except
        Args:
            id_(UUID): Indentificator
            exception (WRKFEception): Custom Exception
        Exception:
            NodeNotExists
        """
        instance = await self.repository.get_by_id(id_)
        if instance:
            return instance

        if exception is None:
            raise NodeNotExists()
        raise exception()

    async def exists(self, **filters) -> bool:
        """
        Check if record exists in database
        Args:
            **filters(Dict[str, str]): Key is column of table and value is value. Example: id=1
        Return:
            bool: Is object exists
        """
        return await self.repository.exists(**filters)
