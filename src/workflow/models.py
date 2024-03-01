from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, MetaData, Table, UUID, func, text

from src.models import uuid
from src.workflow.constants import MessageStatus, NodeType

metadata_obj = MetaData()

class Node(Base):
    """Node model"""
    __tablename__ = "nodes"
    node_type: Mapped[NodeType]

class MessageNode(Node):
    __tablename__ = "message_node"
    id: Mapped[uuid] = mapped_column(ForeignKey("nodes.id"), primary_key=True)

    status: Mapped[MessageStatus] = mapped_column(nullable=True)
    text: Mapped[str]

class ConditionNode(Node):
    __tablename__ = "condition_node"

    id: Mapped[uuid] = mapped_column(ForeignKey("nodes.id"), primary_key=True)


class Edge(Base):
    __tablename__ = 'edges'
    from_node_id: Mapped[uuid] = mapped_column(ForeignKey('nodes.id'))
    to_node_id:  Mapped[uuid] = mapped_column(ForeignKey('nodes.id'))

    from_node = relationship('Node', foreign_keys=[from_node_id])
    to_node = relationship('Node', foreign_keys=[to_node_id])


class Workflow(Base):
    __tablename__ = "workflow"

    name: Mapped[str] = mapped_column(unique=True)
