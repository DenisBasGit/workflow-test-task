from fastapi import HTTPException, status

class WorkflowNotFoundHTTPExeception(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Workflow Not Found"
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
