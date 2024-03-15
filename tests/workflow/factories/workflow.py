import factory
from factory.alchemy import SQLAlchemyModelFactory

from src.workflow.models import Workflow


class WorkflowFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Workflow

    name = factory.Sequence(lambda n: f"Workflow-{n}")
