from enum import Enum

import matplotlib.pyplot as plt
import networkx as nx


class NodeType(Enum):
    START = "Start"
    MESSAGE = "Message"
    CONDITION = "Condition"
    END = "End"


class MessageStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"


class StartNode:
    def __init__(self):
        self.type = NodeType.START

    def __str__(self):
        return self.type.value


class MessageNode:
    def __init__(self, text, status=MessageStatus.PENDING):
        self.type = NodeType.MESSAGE
        self.text = text
        self.status = status

    def __str__(self):
        return self.type.value


class ConditionNode:
    def __init__(self, condition):
        self.type = NodeType.CONDITION
        self.condition = condition

    def __str__(self):
        return self.type.value


class EndNode:
    def __init__(self):
        self.type = NodeType.END

    def __str__(self):
        return self.type.value


G = nx.DiGraph()

# Додавання вузлів до графу
start_node = StartNode()
message_node_pending = MessageNode("How are you ?", MessageStatus.PENDING)
message_node_opened = MessageNode("Hello", MessageStatus.OPENED)
message_node_old = MessageNode("How old are you", MessageStatus.PENDING)
message_node_pets = MessageNode("Do you like Pets", MessageStatus.PENDING)
condition_node = ConditionNode(True)
second_condition_node = ConditionNode(True)
end_node = EndNode()

G.add_node(start_node)
G.add_node(message_node_pending)
G.add_node(message_node_opened)
G.add_node(condition_node)
G.add_node(end_node)

# Додавання ребер між вузлами
G.add_edge(start_node, message_node_opened)
G.add_edge(message_node_opened, condition_node)
G.add_edge(condition_node, message_node_pending, label="Yes")
G.add_edge(condition_node, second_condition_node, label="No")
G.add_edge(second_condition_node, message_node_old, label="Yes")
G.add_edge(second_condition_node, message_node_pets, label="No")
G.add_edge(message_node_pets, end_node)
G.add_edge(message_node_old, end_node)
G.add_edge(message_node_pending, end_node)


# G.add_edge(message_node, end_node)

# Додавання умовних ребер для ConditionNode
# G.add_edge(condition_node, message_node, label="Yes")
# G.add_edge(condition_node, end_node, label="No")

# Виведення графу
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Показати граф
plt.show()
