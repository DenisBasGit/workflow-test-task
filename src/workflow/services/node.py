from src.utils.repository import GenericSqlRepository
from sqlalchemy.ext.asyncio import AsyncSession

from src.workflow.repositories import WorkflowRepository
from src.workflow.services import WorkflowService
from src.workflow.services.exceptions import WorkflowNotExists, UnableCreateNodeException
from src.workflow.constants import NodeType


class NodeService:

    def __init__(self, session: AsyncSession, repository):
        self.session = session
        self.repository: GenericSqlRepository = repository(self.session)
        self.workflow_service = WorkflowService(self.session)

    async def create(self, data) -> str:
        validated_data = await self.validate(data)
        node = await self.repository.add(validated_data)
        await self.session.commit()
        return node

    async def update(self, id, data):
        validated_data = data.model_dump()
        record = await self.repository.get_by_id(id)
        if record is None:
            raise WorkflowNotExists()
        for attr, value in validated_data.items():
            setattr(record, attr, value)
        workflow = await self.repository.update(record)
        return workflow

    async def delete(self, id) -> None:
        record = await self.repository.get_by_id(id)
        if record is None:
            raise WorkflowNotExists()
        await self.repository.delete(record)
        await self.session.commit()

    async def validate(self, data):
        """Validate nodes"""
        validate_data = data.model_dump()
        is_workflow_exists = await self.workflow_service.exists(id=validate_data["workflow_id"])
        if not is_workflow_exists:
            raise WorkflowNotExists()
        if validate_data["type"] in (NodeType.START, NodeType.END):
            is_node_exists = await self.exists(
                type=validate_data["type"],
                workflow_id=validate_data["workflow_id"]
            )
            if is_node_exists:
                raise UnableCreateNodeException()
        return validate_data

    async def exists(self, **filter) -> bool:
        return await self.repository.exists(**filter)