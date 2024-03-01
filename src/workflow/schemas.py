from pydantic import BaseModel

class WorkflowSchema(BaseModel):
    name: str

class CreateWorkflowSchema(WorkflowSchema):
    """Create workflow schema"""

class UpdateWorkflowSchema(WorkflowSchema):
    """Update workflow schema"""
