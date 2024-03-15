from fastapi import status

from src.exceptions import WRKFEception


class WorkflowNotExists(WRKFEception):
    """Workflow not Exists"""

    status_code = status.HTTP_404_NOT_FOUND


class WorkflowAlreadyExists(WRKFEception):
    """Workflow already exists"""

    message = "Workflow already exists"
    status_code = status.HTTP_400_BAD_REQUEST


class UnableCreateNodeException(WRKFEception):
    """Unable to create node. Nodes with type start and end should be only 1"""

    status_code = status.HTTP_400_BAD_REQUEST


class NodeNotExists(WRKFEception):
    """Node not Exists"""

    status_code = status.HTTP_404_NOT_FOUND


class EdgeNotExists(WRKFEception):
    """Edge not Exists"""


class UnableCreateEdgeExeption(WRKFEception):
    """Ubable create edge exception"""

    status_code = status.HTTP_400_BAD_REQUEST


class StartEdgeCannotHaveIncomingException(WRKFEception):
    """Start edge cannot have incoming relation exception"""

    status_code = status.HTTP_400_BAD_REQUEST


class EndEdgeCannotHaveOutputException(WRKFEception):
    """End edge cannot have Output relation exception"""

    status_code = status.HTTP_400_BAD_REQUEST
