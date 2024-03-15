import src.handlers  # noqa pylint: disable=W0611
from src.core import app
from src.workflow.router import router as workflow_router

__all__ = [
    "app",
]

app.include_router(workflow_router)
