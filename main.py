from fastapi import FastAPI
import networkx as nx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

building = nx.Graph()

building.add_node("Main Gate", pos=(14.3,4.0), label='Main Gate')
building.add_node("Dining Area", pos=(46,4), label='Dining Area')
building.add_node("Living Room", pos=(24,4), label='Living Room')
building.add_node("Front Closet", pos=(24,16), label='Front Closet')
building.add_node("Kitchen and Dining Junction", pos=(46, 16), label='Kitchen and Dining Junction')
building.add_node("Kitchen", pos=(46, 23), label='Kitchen')
building.add_node("Bedroom 1", pos=(37,33), label='Bedroom 1')
building.add_node("Bedroom 2", pos=(46,33), label='Bedroom 2')
building.add_node("Bedroom 3", pos=(74,33), label='Bedroom 3')

building.add_edge("Living Room", "Main Gate")
building.add_edge("Living Room", "Dining Area")
building.add_edge("Living Room", "Front Closet")
building.add_edge("Dining Area", "Kitchen and Dining Junction")
building.add_edge("Front Closet", "Kitchen and Dining Junction")
# building.add_edge("Bedroom 1", "Kitchen and Dining Junction")
building.add_edge("Bedroom 2", "Kitchen and Dining Junction")
building.add_edge("Bedroom 1", "Bedroom 2")
building.add_edge("Bedroom 3", "Bedroom 2")
building.add_edge("Kitchen", "Kitchen and Dining Junction")
building.add_edge("Kitchen", "Bedroom 2")



@app.get('/find_route')
def shortest_path(startNode: str, endNode: str):
    path = nx.shortest_path(building, source = startNode, target = endNode)
    path_with_coord = []
    for node in path:
        path_with_coord.append({
            "name": node,
            "coords": building.nodes[node]["pos"]
        })
    return {"status": "success", "route": path_with_coord}

@app.get("/search_rooms")
def search_rooms():
    return [{"id":n, "label": building.nodes[n].get('label',n)} for n in building.nodes]