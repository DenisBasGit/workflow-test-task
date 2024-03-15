import uuid

import pytest
from fastapi import status
from httpx import AsyncClient

from src.workflow.models import Workflow
from tests.test_types import DBInsert
from tests.workflow.factories.workflow import WorkflowFactory

PATH_WORKFLOW = "/workflow"
PATH_WORKFLOW_DETAIL = PATH_WORKFLOW + "/%s"


@pytest.mark.asyncio
class TestCreateWorkflow:
    @pytest.fixture
    async def workflow(self, db_ins: DBInsert) -> Workflow:
        return await db_ins(WorkflowFactory)

    async def test_url(self, client: AsyncClient):
        response = await client.post(PATH_WORKFLOW)
        assert response.status_code not in (status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_create_workflow_success(self, client: AsyncClient) -> None:
        payload = {"name": "Test"}
        response = await client.post(PATH_WORKFLOW, json=payload)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_workflow_with_already_used_name(self, workflow: Workflow, client: AsyncClient) -> None:
        payload = {"name": workflow.name}
        response = await client.post(PATH_WORKFLOW, json=payload)
        assert response.status_code == 400


class TestUpdateWorkflow:
    @pytest.fixture
    async def workflow(self, db_ins: DBInsert) -> Workflow:
        return await db_ins(WorkflowFactory)

    async def test_url(self, workflow: Workflow, client: AsyncClient):
        response = await client.put(PATH_WORKFLOW_DETAIL % workflow.id)
        assert response.status_code not in (status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED)

    @pytest.mark.asyncio
    async def test_update_workflow_success(self, workflow: Workflow, client: AsyncClient) -> None:
        PATH_WORKFLOW_ID = PATH_WORKFLOW + f"/{workflow.id}"
        payload = {"name": "New Name"}
        response = await client.put(PATH_WORKFLOW_ID, json=payload)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_not_exists_workflow(self, client: AsyncClient) -> None:
        PATH_WORKFLOW_ID = PATH_WORKFLOW + f"/{uuid.uuid4()}"
        payload = {"name": "New Name"}
        response = await client.put(PATH_WORKFLOW_ID, json=payload)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_workflow_with_empty_data(self, workflow: Workflow, client: AsyncClient) -> None:
        PATH_WORKFLOW_ID = PATH_WORKFLOW + f"/{workflow.id}"
        payload = {}
        response = await client.put(PATH_WORKFLOW_ID, json=payload)
        assert response.status_code == 422


class TestDeleteWorkflow:
    @pytest.fixture
    async def workflow(self, db_ins: DBInsert) -> Workflow:
        return await db_ins(WorkflowFactory)

    async def test_url(self, workflow: Workflow, client: AsyncClient):
        response = await client.delete(PATH_WORKFLOW_DETAIL % workflow.id)
        assert response.status_code not in (status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED)

    @pytest.mark.asyncio
    async def test_delete_workflow_success(self, workflow: Workflow, client: AsyncClient) -> None:
        PATH_WORKFLOW_ID = PATH_WORKFLOW + f"/{workflow.id}"
        response = await client.delete(PATH_WORKFLOW_ID)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_not_exists_workflow(self, client: AsyncClient) -> None:
        PATH_WORKFLOW_ID = PATH_WORKFLOW + f"/{uuid.uuid4()}"
        response = await client.delete(PATH_WORKFLOW_ID)
        assert response.status_code == 404
