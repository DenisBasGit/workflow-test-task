import uuid
from typing import Tuple

import pytest
from fastapi import status
from httpx import AsyncClient

from src.workflow.constants import MessageStatus, NodeType
from src.workflow.models import Node, Workflow
from tests.test_types import DBInsert
from tests.workflow.factories.node import StartNodeFactory
from tests.workflow.factories.workflow import WorkflowFactory

PATH_NODE = "workflow/node"
PATH_NODE_DETAIL = PATH_NODE + "/%s"


@pytest.fixture
async def workflow(db_ins: DBInsert) -> Workflow:
    return await db_ins(WorkflowFactory)


@pytest.fixture
async def node(workflow: Workflow, db_ins: DBInsert) -> Tuple[Workflow, Node]:
    node = await db_ins(StartNodeFactory, workflow_id=workflow.id)
    return workflow, node


@pytest.mark.asyncio
class TestCreateNode:
    async def test_url(self, client: AsyncClient):
        response = await client.post(PATH_NODE)
        assert response.status_code not in (status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_create_node_success(self, workflow: Workflow, client: AsyncClient):
        payload = {
            "workflow_id": str(workflow.id),
            "type": NodeType.START,
            "message": "Test",
            "status": MessageStatus.OPENED,
        }
        response = await client.post(PATH_NODE, json=payload)
        assert response.status_code == 201

    async def test_create_with_not_exists_workflow(self, client: AsyncClient):
        payload = {
            "workflow_id": str(uuid.uuid4()),
            "type": NodeType.START,
            "message": "Test",
            "status": MessageStatus.OPENED,
        }
        response = await client.post(PATH_NODE, json=payload)
        assert response.status_code == 400

    async def test_create_node_with_already_exists_node_type(self, node: Node, client: AsyncClient):
        workflow, node = node
        payload = {
            "workflow_id": str(workflow.id),
            "type": node.type,
        }
        response = await client.post(PATH_NODE, json=payload)
        assert response.status_code == 400


class TestDeleteNode:
    async def test_url(self, node: Node, client: AsyncClient):
        _, node = node
        response = await client.delete(PATH_NODE_DETAIL % node.id)
        assert response.status_code not in (status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_delete_node_success(self, node: Node, client: AsyncClient):
        _, node = node
        response = await client.delete(PATH_NODE_DETAIL % str(node.id))
        assert response.status_code == 204

    async def test_delete_node_not_exists(self, client: AsyncClient):
        response = await client.delete(PATH_NODE_DETAIL % uuid.uuid4())
        assert response.status_code == 404
