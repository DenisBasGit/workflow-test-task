import uuid

from src.utils.exceptions import NotFoundException
from src.utils.repository import GenericSqlRepository
from sqlalchemy.ext.asyncio import AsyncSession

from src.workflow.services.exceptions import WorkflowNotExists


class WorkflowService:

    def __init__(self, session: AsyncSession, repository):
        self.session = session
        self.repository: GenericSqlRepository = repository(self.session)

    async def create(self, data) -> str:
        validated_data = data.model_dump()
        workflow_id = await self.repository.add(validated_data)
        await self.session.commit()
        return workflow_id

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
