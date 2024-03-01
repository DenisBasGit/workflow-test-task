from typing import Annotated
from fastapi import Depends
from src.workflow.repositories import WorkflowRepository
from src.workflow.services import WorkflowService
from src.dependencies import DatabaseDep

__all__ = [
    "WorkflowDep"
]


def workflow_service(db: DatabaseDep):
    return WorkflowService(db, WorkflowRepository)


WorkflowDep = Annotated[WorkflowService, Depends(workflow_service)]
