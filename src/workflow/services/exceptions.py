class WorkflowNotExists(Exception):
    """Workflow not Exists"""

class UnableCreateNodeException(Exception):
    """Unable to create node. Nodes with type start and end should be only 1"""