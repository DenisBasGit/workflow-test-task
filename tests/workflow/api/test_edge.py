import uuid

import pytest
from fastapi import status
from httpx import AsyncClient

from src.workflow.models import Workflow
from tests.test_types import DBInsert
from tests.workflow.factories import (
    ConditionNodeFactory,
    EdgeFactory,
    EndNodeFactory,
    MessageNodeFactory,
    StartNodeFactory,
    WorkflowFactory,
)

PATH_EDGE = "workflow/edge"


@pytest.fixture
async def workflow(db_ins: DBInsert):
    return await db_ins(WorkflowFactory)


@pytest.mark.asyncio
class TestCreateEdge:
    async def test_url(self, client: AsyncClient):
        response = await client.post(PATH_EDGE)
        assert response.status_code not in [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED]

    async def test_create_edge_success(self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient):
        node_from = await db_ins(StartNodeFactory, workflow_id=workflow.id)
        node_to = await db_ins(MessageNodeFactory, workflow_id=workflow.id)

        payload = {"from_node_id": str(node_from.id), "to_node_id": str(node_to.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_with_not_exists_nodes(self, client: AsyncClient):
        payload = {"from_node_id": str(uuid.uuid4()), "to_node_id": str(uuid.uuid4())}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_edge_between_nodes_from_other_workflow(self, db_ins: DBInsert, client: AsyncClient):
        first_workflow = await db_ins(WorkflowFactory)
        second_workflow = await db_ins(WorkflowFactory)
        from_node = await db_ins(StartNodeFactory, workflow_id=first_workflow.id)
        to_node = await db_ins(MessageNodeFactory, workflow_id=second_workflow.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_edge_with_from_node_end(self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient):
        from_node = await db_ins(EndNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(MessageNodeFactory, workflow_id=workflow.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_edge_with_to_node_start(self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient):
        from_node = await db_ins(MessageNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(StartNodeFactory, workflow_id=workflow.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_second_edge_from_message_node(
        self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient
    ):
        from_node = await db_ins(MessageNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        another_condition_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        await db_ins(EdgeFactory, from_node_id=from_node.id, to_node_id=another_condition_node.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_edge_between_condition_node_and_start_node(
        self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient
    ):
        from_node = await db_ins(StartNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_edge_between_condition_node_and_message_node(
        self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient
    ):
        from_node = await db_ins(MessageNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_edge_between_condition_node_and_condition_node(
        self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient
    ):
        from_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_second_edge_for_condition_node(
        self, db_ins: DBInsert, workflow: Workflow, client: AsyncClient
    ):
        from_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        to_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        end_node = await db_ins(EndNodeFactory, workflow_id=workflow.id)
        condition_node = await db_ins(ConditionNodeFactory, workflow_id=workflow.id)
        await db_ins(EdgeFactory, from_node_id=from_node.id, to_node_id=end_node.id)
        await db_ins(EdgeFactory, from_node_id=from_node.id, to_node_id=condition_node.id)
        payload = {"from_node_id": str(from_node.id), "to_node_id": str(to_node.id)}
        response = await client.post(PATH_EDGE, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
