from enum import Enum


class NodeType(str, Enum):
    """Enum class for node type"""

    START = "Start"
    MESSAGE = "Message"
    CONDITION = "Condition"
    END = "End"


class MessageStatus(str, Enum):
    """Enum class for message status"""

    PENDING = "Pending"
    SENT = "Sent"
    OPENED = "Opened"
