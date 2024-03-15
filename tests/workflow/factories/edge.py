from factory.alchemy import SQLAlchemyModelFactory

from src.workflow.models import Edge


class EdgeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Edge
