from fastapi import HTTPException, status

class WorkflowNotFoundHTTPExeception(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Workflow Not Found"
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UnableCreateNodeHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Workflow cannot have more than 1 'start' and 'end' node"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)