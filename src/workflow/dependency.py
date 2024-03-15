from typing import Annotated

from fastapi import Depends

from src.dependencies import DatabaseDep
from src.workflow.repositories import EdgeRepository, NodeRepository, WorkflowRepository
from src.workflow.services import EdgeService, NodeService, WorkflowService

__all__ = [
    "WorkflowDependency",
    "NodeDependency",
    "EdgeDependency",
]


def workflow_service(db: DatabaseDep):
    """Workflow service for dependency"""
    return WorkflowService(db, WorkflowRepository)


def node_service(db: DatabaseDep):
    """Node service for dependency"""
    return NodeService(db, NodeRepository)


def edge_service(db: DatabaseDep):
    """Edge service for dependency"""
    return EdgeService(db, EdgeRepository)


WorkflowDependency = Annotated[WorkflowService, Depends(workflow_service)]

NodeDependency = Annotated[NodeService, Depends(node_service)]

EdgeDependency = Annotated[EdgeService, Depends(edge_service)]
