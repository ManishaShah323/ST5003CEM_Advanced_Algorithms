import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq
import math

# =====================================================
# TASK 6 – GRAPH SEARCH (POLAND MAP)
# =====================================================

START = "Glogow"
GOAL = "Plock"

# =====================================================
# STATE SPACE (GRAPH WITH COSTS)
# =====================================================
GRAPH = {
    "Glogow": {"Leszno": 45, "Wroclaw": 40},
    "Leszno": {"Glogow": 45, "Poznan": 90, "Kalisz": 140},
    "Wroclaw": {"Glogow": 40, "Opole": 80},
    "Poznan": {"Leszno": 90, "Bydgoszcz": 110, "Konin": 120},
    "Bydgoszcz": {"Poznan": 110, "Wloclawek": 100},
    "Wloclawek": {"Bydgoszcz": 100, "Plock": 55},
    "Plock": {"Wloclawek": 55, "Warsaw": 130},
    "Warsaw": {"Plock": 130, "Lodz": 150, "Radom": 105},
    "Radom": {"Warsaw": 105, "Kielce": 82},
    "Kielce": {"Radom": 82, "Krakow": 120},
    "Krakow": {"Kielce": 120, "Katowice": 85},
    "Katowice": {"Krakow": 85, "Czestochowa": 68, "Opole": 118},
    "Czestochowa": {"Katowice": 68, "Kalisz": 160},
    "Kalisz": {"Leszno": 140, "Lodz": 128, "Czestochowa": 160},
    "Lodz": {"Warsaw": 150, "Konin": 120, "Kalisz": 128},
    "Konin": {"Poznan": 120, "Lodz": 120},
    "Opole": {"Wroclaw": 80, "Katowice": 118}
}

# =====================================================
# NODE POSITIONS (FOR HEURISTIC)
# =====================================================
POS = {
    "Glogow": (0,4), "Leszno": (1,5), "Poznan": (2,6),
    "Bydgoszcz": (3,7), "Wloclawek": (4,6), "Plock": (5,6),
    "Warsaw": (6,5), "Radom": (6,4), "Kielce": (6,3),
    "Krakow": (5,2), "Katowice": (4,2), "Czestochowa": (3,3),
    "Kalisz": (2,4), "Konin": (3,4), "Lodz": (4,4),
    "Wroclaw": (0,3), "Opole": (1,3)
}

# =====================================================
# PATH RECONSTRUCTION
# =====================================================
def reconstruct_path(parent, start, goal):
    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

# =====================================================
# DFS (STACK, FIRST-GOAL TERMINATION)
# =====================================================
def dfs_search(graph, start, goal):
    stack = [(start, 0)]
    closed = set()
    parent = {start: None}
    edges = []

    while stack:
        node, cost = stack.pop()

        if node == goal:
            return edges, reconstruct_path(parent, start, goal), cost

        if node in closed:
            continue

        closed.add(node)

        # reverse sorted → deterministic DFS order
        for nbr, w in sorted(graph[node].items(), reverse=True):
            if nbr not in closed:
                parent[nbr] = node
                edges.append((node, nbr))
                stack.append((nbr, cost + w))

    return edges, [], float("inf")

# =====================================================
# BFS (QUEUE, LEVEL-ORDER SEARCH)
# =====================================================
def bfs_search(graph, start, goal):
    queue = deque([(start, 0)])
    closed = {start}
    parent = {start: None}
    edges = []

    while queue:
        node, cost = queue.popleft()

        if node == goal:
            return edges, reconstruct_path(parent, start, goal), cost

        for nbr, w in sorted(graph[node].items()):
            if nbr not in closed:
                closed.add(nbr)
                parent[nbr] = node
                edges.append((node, nbr))
                queue.append((nbr, cost + w))

    return edges, [], float("inf")

# =====================================================
# A* SEARCH (OPTIMAL COST)
# =====================================================
def heuristic(a, b):
    return math.dist(POS[a], POS[b])

def a_star_search(graph, start, goal):
    open_heap = [(heuristic(start, goal), start)]
    parent = {start: None}
    g_cost = {start: 0}
    closed = set()
    edges = []

    while open_heap:
        _, node = heapq.heappop(open_heap)

        if node == goal:
            return edges, reconstruct_path(parent, start, goal), g_cost[node]

        if node in closed:
            continue

        closed.add(node)

        for nbr, w in graph[node].items():
            tentative_g = g_cost[node] + w
            if nbr not in g_cost or tentative_g < g_cost[nbr]:
                g_cost[nbr] = tentative_g
                f = tentative_g + heuristic(nbr, goal)
                heapq.heappush(open_heap, (f, nbr))
                parent[nbr] = node
                edges.append((node, nbr))

    return edges, [], float("inf")

# =====================================================
# RUN SEARCHES
# =====================================================
dfs_edges, dfs_path, dfs_cost = dfs_search(GRAPH, START, GOAL)
bfs_edges, bfs_path, bfs_cost = bfs_search(GRAPH, START, GOAL)
astar_edges, astar_path, astar_cost = a_star_search(GRAPH, START, GOAL)

print("\nDFS Path :", " -> ".join(dfs_path), "| Cost:", dfs_cost)
print("BFS Path :", " -> ".join(bfs_path), "| Cost:", bfs_cost)
print("A*  Path :", " -> ".join(astar_path), "| Cost:", astar_cost)

# =====================================================
# VISUALIZATION: STATE SPACE
# =====================================================
G = nx.Graph()
for u in GRAPH:
    for v, w in GRAPH[u].items():
        G.add_edge(u, v, weight=w)

plt.figure(figsize=(12, 8))
nx.draw(
    G, POS, with_labels=True,
    node_color=[
        "skyblue" if n == START else
        "red" if n == GOAL else
        "lightgray" for n in G.nodes()
    ],
    node_size=1600,
    edgecolors="black"
)
nx.draw_networkx_edge_labels(
    G, POS,
    edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
)
plt.title("State Space Graph (Poland Map)", fontweight="bold")
plt.axis("off")
plt.show()
