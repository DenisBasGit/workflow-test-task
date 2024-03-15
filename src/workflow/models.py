from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, func, select
from sqlalchemy.ext.asyncio import async_object_session
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.workflow.constants import MessageStatus, NodeType


class Edge(Base):
    """Edge Model"""

    __tablename__ = "edges"
    label: Mapped[str] = mapped_column(nullable=True)
    from_node_id: Mapped[UUID] = mapped_column(ForeignKey("nodes.id"))
    to_node_id: Mapped[UUID] = mapped_column(ForeignKey("nodes.id"))

    from_node = relationship("Node", foreign_keys=[from_node_id])
    to_node = relationship("Node", foreign_keys=[to_node_id])

    __table_args__ = (UniqueConstraint("from_node_id", "to_node_id", name="unique_edge"),)


class Node(Base):
    """Node Model"""

    __tablename__ = "nodes"
    workflow_id: Mapped[UUID] = mapped_column(ForeignKey("workflow.id"))
    type: Mapped[NodeType]
    text: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[MessageStatus] = mapped_column(nullable=True)

    workflow = relationship("Workflow", foreign_keys=[workflow_id])

    edges_from = relationship("Edge", foreign_keys="[Edge.from_node_id]", overlaps="from_node")
    edges_to = relationship("Edge", foreign_keys="[Edge.to_node_id]", overlaps="to_node")

    @property
    async def edges_from_count(self) -> int:
        """
        Edges from count
        method to count how many edges output have node
        """
        # pylint: disable=E1102
        return await async_object_session(self).scalar(  # type: ignore
            select(func.count(Edge.id)).where(Edge.from_node_id == self.id)
        )

    @property
    async def edges_to_count(self) -> int:
        """
        Edges to count
        method to count how many edges incoming have node
        """
        # pylint: disable=E1102
        return await async_object_session(self).scalar(  # type: ignore
            select(func.count(Edge.id)).where(Edge.to_node_id == self.id)
        )


class Workflow(Base):
    """Worflow model"""

    __tablename__ = "workflow"
    name: Mapped[str] = mapped_column(unique=True)
