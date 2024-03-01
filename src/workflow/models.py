import uuid
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, MetaData, Table, UUID, func, text
from src.workflow.constants import MessageStatus, NodeType

metadata_obj = MetaData()

class Node(Base):
    __tablename__ = 'nodes'

    workflow_id: Mapped[uuid] = mapped_column(ForeignKey('workflow.id'))
    type: Mapped[NodeType]
    text: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[MessageStatus] = mapped_column(nullable=True)

    workflow = relationship("Workflow", foreign_keys=[workflow_id])

class Edge(Base):
    __tablename__ = 'edges'

    from_node_id: Mapped[uuid] = mapped_column(ForeignKey('nodes.id'))
    to_node_id: Mapped[uuid] = mapped_column(ForeignKey('nodes.id'))

    from_node = relationship("Node", foreign_keys=[from_node_id])
    to_node = relationship("Node", foreign_keys=[to_node_id])


class Workflow(Base):
    __tablename__ = "workflow"

    name: Mapped[str] = mapped_column(unique=True)
