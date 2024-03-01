from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.workflow.router import router as workflow_router
import networkx as nx
import matplotlib.pyplot as plt

app = FastAPI()

app.include_router(workflow_router)


# @app.get("/test")
# async def test():
#     G = nx.Graph()
#     G.add_node("Singapore")
#     G.add_node("San Francisco")
#     G.add_node("Tokyo")
#     G.add_nodes_from(["Riga", "Copenhagen"])
#     nx.draw(G)
#     plt.show()
#     return JSONResponse({"test": "Test"})