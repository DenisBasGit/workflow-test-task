from typing import Any, Callable, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.workflow.models import Workflow
from src.workflow.repositories import WorkflowRepository
from src.workflow.schemas import CreateWorkflowSchema, UpdateWorkflowSchema
from src.workflow.services.exceptions import WorkflowAlreadyExists, WorkflowNotExists


class WorkflowService:
    """Workflow Service"""

    def __init__(self, session: AsyncSession, repository: Callable[[AsyncSession], WorkflowRepository] | None = None):
        self.session = session
        if repository is None:
            repository = WorkflowRepository
        self.repository = repository(self.session)

    async def validate(self, data: CreateWorkflowSchema) -> Dict[str, Any]:
        """
        Validate
        Args:
            data(CreateWorkflowSchema) -> Data for create record
        Return:
            validated_data(Dict[str, Any]): Validated data
        """
        valdiated_data = data.model_dump()
        if await self.repository.exists(name=valdiated_data["name"]):
            raise WorkflowAlreadyExists()
        return valdiated_data

    async def create(self, data: CreateWorkflowSchema) -> Workflow:
        """
        Create Record
        Args:
            data(CreateWorkflowSchema) -> Data for create record
        Return:
            Workflow: New Record
        """
        validated_data = await self.validate(data)
        workflow = await self.repository.add(validated_data)
        await self.session.commit()
        return workflow

    async def update(self, id_: UUID, data: UpdateWorkflowSchema) -> Workflow:
        """
        Update Record
        Args:
            id_(UUID): Indentificator
            data(UpdateWorkflowSchema): Data for create record
        Return:
            Workflow: Updated Record
        Exception:
            WorkflowNotExists: When record not found
        """
        validated_data = data.model_dump()
        record = await self.repository.get_by_id(id_)
        if record is None:
            raise WorkflowNotExists()
        for attr, value in validated_data.items():
            setattr(record, attr, value)
        workflow = await self.repository.update(record)
        return workflow

    async def delete(self, id_: UUID) -> None:
        """
        Delete Record from database
        Args:
            id_: Indentificator of table
        Exception:
            WorkflowNotExists - when record not found
        """
        record = await self.repository.get_by_id(id_)
        if record is None:
            raise WorkflowNotExists()
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
