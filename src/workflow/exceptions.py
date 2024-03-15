from typing import Optional

from fastapi import HTTPException, status


class WorkflowNotFoundHTTPExeception(HTTPException):
    """Workflow not found http Exeception"""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Workflow Not Found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UnableCreateNodeHTTPException(HTTPException):
    """Unable create node Http Exeception"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Workflow cannot have more than 1 'start' and 'end' node"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UnableCreateEdgeHTTPException(HTTPException):
    """Unable create edge Http Exeception"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Edge cannot be create. This relation already exists"

    def __init__(self, message: Optional[str] = None):
        if message:
            self.detail = message
        super().__init__(status_code=self.status_code, detail=self.detail)


class StartNodeCannotHaveIncomingHTTPException(HTTPException):
    """Start Node Cannot have incoming edge Http Exeception"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Edge cannot be create. Start node cannot have incoming relation"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class EndNodeCannotHaveOutputHTTPException(HTTPException):
    """End Node Cannot have output edge Http Exeception"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Edge cannot be create. End node cannot have incoming relation"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
