import matplotlib.pyplot as plt
import networkx as nx


def create_workflow_graph(workflow_data):
    """TEst"""
    graph = nx.DiGraph()
    for node in workflow_data["nodes"]:
        graph.add_node(node["type"])
        for edge in node.get("edges", []):
            graph.add_edge(node["type"], edge)
    return graph


def find_path_in_workflow(graph, start_node="Start", end_node="End"):
    """TEst"""
    try:
        path = nx.shortest_path(graph, source=start_node, target=end_node)
        return path
    except nx.NetworkXNoPath:
        return None


# Example workflow data
workflow_data = {
    "nodes": [
        {"type": "Start", "edges": ["Message1"]},
        {"type": "Message1", "edges": ["Condition1"]},
        {"type": "Condition1", "edges": ["Message2", "End"]},
        {"type": "Message2", "edges": ["End"]},
        {"type": "End"},
    ]
}

# Create a graph from the workflow data
workflow_graph = create_workflow_graph(workflow_data)
nx.draw_shell(workflow_graph)
plt.show()
# Find the path from the start node to the end node
path = find_path_in_workflow(workflow_graph)
if path:
    print(f"Path found: {path}")
else:
    print("No path found")

workflow_data = {
    "nodes": [
        {"type": "Start", "edges": ["Message1"]},
        {"type": "Message1", "edges": ["Condition1"], "status": "(Pending, Sent, Opened)"},
        {"type": "Condition1", "edges": ["Message2", "End"]},
        {"type": "Message2", "edges": ["End"]},
        {"type": "End"},
    ]
}
