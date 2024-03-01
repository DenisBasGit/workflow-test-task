import uuid

from fastapi import APIRouter, status, Response

from src.workflow.dependency import WorkflowDep
from src.workflow.exceptions import WorkflowNotFoundHTTPExeception
from src.workflow.schemas import CreateWorkflowSchema, UpdateWorkflowSchema
from src.workflow.services.exceptions import WorkflowNotExists

router = APIRouter(
    prefix="/workflow",
    tags=["workflow"]
)


@router.post("")
async def create_workflow(service: WorkflowDep, workflow: CreateWorkflowSchema):
    workflow_id = await service.create(workflow)
    return {"id": workflow_id}

@router.put("/{workflow_id}", status_code=status.HTTP_200_OK)
async def update_workflow(service: WorkflowDep, workflow_id, data: UpdateWorkflowSchema):
    try:
        record = await service.update(workflow_id, data)
    except WorkflowNotExists:
        raise WorkflowNotFoundHTTPExeception()
    return record


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(service: WorkflowDep, workflow_id):
    try:
        await service.delete(workflow_id)
    except WorkflowNotExists:
        raise WorkflowNotFoundHTTPExeception()
    return Response(status_code=status.HTTP_204_NO_CONTENT)