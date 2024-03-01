import uuid
from typing import Optional

from pydantic import BaseModel, Field

from src.workflow.constants import NodeType, MessageStatus


class WorkflowSchema(BaseModel):
    name: str

class CreateWorkflowSchema(WorkflowSchema):
    """Create workflow schema"""

class UpdateWorkflowSchema(WorkflowSchema):
    """Update workflow schema"""

class CreateNodeSchema(BaseModel):
    """Node schema"""
    workflow_id: str
    type: NodeType
    text: Optional[str] = Field(default=None)
    status: Optional[MessageStatus] = Field(default=None)
