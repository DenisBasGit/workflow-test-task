from enum import Enum


class NodeType(str, Enum):
     START = "Start"
     MESSAGE = "Message"
     CONDITION = "Condition"
     END = "End"

class MessageStatus(str, Enum):
     PENDING = "Pending"
     SENT = "Sent"
     OPENED = "Opened"