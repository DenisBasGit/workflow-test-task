from typing import Any, Dict
from uuid import UUID

import networkx as nx
from fastapi import APIRouter, status

from src.workflow.constants import NodeType
from src.workflow.dependency import EdgeDependency, NodeDependency, WorkflowDependency
from src.workflow.schemas import (
    CreateEdgeSchema,
    CreateNodeSchema,
    CreateWorkflowSchema,
    UpdateWorkflowSchema,
)

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_workflow(service: WorkflowDependency, workflow: CreateWorkflowSchema):
    """
    Create workflow
    """
    workflow_id = await service.create(workflow)
    return {"id": workflow_id}


@router.put("/{workflow_id}", status_code=status.HTTP_200_OK)
async def update_workflow(service: WorkflowDependency, workflow_id, data: UpdateWorkflowSchema):
    """
    Update workflow
    """
    record = await service.update(workflow_id, data)
    return record


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(service: WorkflowDependency, workflow_id) -> None:
    """
    Delete workflow
    """
    await service.delete(workflow_id)


@router.post("/node", status_code=status.HTTP_201_CREATED)
async def create_node(service: NodeDependency, data: CreateNodeSchema) -> Dict[str, Any]:
    """
    Create node
    """
    node_id = await service.create(data)
    return {"id": node_id}


@router.delete("/node/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(service: NodeDependency, node_id: UUID) -> None:
    """
    Create node
    """
    await service.delete(node_id)


@router.post("/edge", status_code=status.HTTP_201_CREATED)
async def create_edge(service: EdgeDependency, data: CreateEdgeSchema) -> Dict[str, Any]:
    """
    Create edge
    """
    edge_id = await service.create(data)
    return {"id": edge_id}


@router.get("/shortest-path/{workflow_id}", status_code=status.HTTP_200_OK)
async def workflow_shortest_path(workflow_id, service_node: NodeDependency, service_edge: EdgeDependency):
    """Get the shortest path from workflow"""
    G = nx.DiGraph()
    nodes = await service_node.list(workflow_id=workflow_id)
    for node in nodes:
        if node.type == NodeType.START:
            start_node = node
        elif node.type == NodeType.END:
            end_node = node
        G.add_node(node.id)

    edges = await service_edge.list()
    for edge in edges:
        G.add_edge(edge.from_node_id, edge.to_node_id, label=edge.label)

    path = nx.shortest_path(G, source=start_node.id, target=end_node.id)
    return path
