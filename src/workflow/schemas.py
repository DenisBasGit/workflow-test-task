import uuid
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

from src.workflow.constants import MessageStatus, NodeType


class WorkflowSchema(BaseModel):
    """Base workflow schema"""

    name: str


class CreateWorkflowSchema(WorkflowSchema):
    """Create workflow schema"""


class UpdateWorkflowSchema(WorkflowSchema):
    """Update workflow schema"""


class CreateNodeSchema(BaseModel):
    """Node schema"""

    workflow_id: uuid.UUID
    type: NodeType
    text: Optional[str] = Field(default=None)
    status: Optional[MessageStatus] = Field(default=None)


class CreateEdgeSchema(BaseModel):
    """Create edge schema"""

    from_node_id: uuid.UUID
    to_node_id: uuid.UUID
    label: Optional[str] = None

    @field_validator("label")
    def validate_label(cls, value):
        """Validate lable"""
        if value is None or value.lower() not in ["yes", "no"]:
            raise ValidationError("Label is required and must be 'yes' or 'no' for nodes of type 'Condition'")
        return value
