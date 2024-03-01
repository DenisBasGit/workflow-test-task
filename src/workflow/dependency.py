from typing import Annotated
from fastapi import Depends
from src.workflow.repositories import WorkflowRepository, NodeRepository
from src.workflow.services import WorkflowService, NodeService
from src.dependencies import DatabaseDep

__all__ = [
    "WorkflowDep"
]


def workflow_service(db: DatabaseDep):
    return WorkflowService(db, WorkflowRepository)

def node_service(db: DatabaseDep):
    return NodeService(db, NodeRepository)


WorkflowDep = Annotated[WorkflowService, Depends(workflow_service)]

NodeDep = Annotated[NodeService, Depends(node_service)]