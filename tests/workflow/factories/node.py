import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory

from src.workflow.constants import MessageStatus, NodeType
from src.workflow.models import Node

from .workflow import WorkflowFactory


class NodeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Node
        # sqlalchemy_session = async_session_maker()

    workflow_id = factory.SubFactory(WorkflowFactory)


class StartNodeFactory(NodeFactory):
    type = NodeType.START.value


class EndNodeFactory(NodeFactory):
    type = NodeType.END.value


class MessageNodeFactory(NodeFactory):
    type = NodeType.MESSAGE.value
    text = factory.fuzzy.FuzzyText(length=20)
    status = factory.fuzzy.FuzzyChoice(choices=MessageStatus)


class ConditionNodeFactory(NodeFactory):
    type = NodeType.CONDITION.value
