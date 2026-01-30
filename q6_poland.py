import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq
import math

# =====================================================
# TASK 6 – GRAPH SEARCH (POLAND MAP)
# =====================================================
# Start City: Glogow
# Goal City : Plock
#
# Visualizations:
# 1. State Space (Map)
# 2. DFS Search Tree
# 3. BFS Search Tree
# 4. A* Search Tree (BONUS)
# =====================================================

# =====================================================
# GRAPH (STATE SPACE)
# =====================================================
graph = {
    "Glogow": ["Leszno", "Wroclaw"],
    "Leszno": ["Glogow", "Poznan", "Kalisz"],
    "Wroclaw": ["Glogow", "Opole"],
    "Poznan": ["Leszno", "Bydgoszcz", "Konin"],
    "Bydgoszcz": ["Poznan", "Wloclawek"],
    "Wloclawek": ["Bydgoszcz", "Plock"],
    "Plock": ["Wloclawek", "Warsaw"],
    "Warsaw": ["Plock", "Lodz", "Radom"],
    "Radom": ["Warsaw", "Kielce"],
    "Kielce": ["Radom", "Krakow"],
    "Krakow": ["Kielce", "Katowice"],
    "Katowice": ["Krakow", "Czestochowa", "Opole"],
    "Czestochowa": ["Katowice", "Kalisz"],
    "Kalisz": ["Leszno", "Lodz", "Czestochowa"],
    "Lodz": ["Warsaw", "Konin", "Kalisz"],
    "Konin": ["Poznan", "Lodz"],
    "Opole": ["Wroclaw", "Katowice"]
}

start = "Glogow"
goal = "Plock"

# =====================================================
# FIXED MAP POSITIONS (USED FOR A* HEURISTIC)
# =====================================================
pos_state = {
    "Glogow": (0,4), "Leszno": (1,5), "Poznan": (2,6), "Bydgoszcz": (3,7),
    "Wloclawek": (4,6), "Plock": (5,6), "Warsaw": (6,5), "Radom": (6,4),
    "Kielce": (6,3), "Krakow": (5,2), "Katowice": (4,2),
    "Czestochowa": (3,3), "Kalisz": (2,4), "Konin": (3,4),
    "Lodz": (4,4), "Wroclaw": (0,3), "Opole": (1,3)
}

# =====================================================
# HELPER: PATH RECONSTRUCTION
# =====================================================
def reconstruct_path(parent, start, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)
    return path[::-1]

# =====================================================
# DFS SEARCH
# =====================================================
def dfs_search(graph, start, goal):
    stack = [start]
    visited = set()
    parent = {start: None}
    edges = []

    while stack:
        node = stack.pop()
        if node == goal:
            break
        if node not in visited:
            visited.add(node)
            for nbr in reversed(graph[node]):
                if nbr not in visited:
                    parent[nbr] = node
                    edges.append((node, nbr))
                    stack.append(nbr)

    return edges, reconstruct_path(parent, start, goal)

# =====================================================
# BFS SEARCH
# =====================================================
def bfs_search(graph, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    edges = []

    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for nbr in graph[node]:
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = node
                edges.append((node, nbr))
                queue.append(nbr)

    return edges, reconstruct_path(parent, start, goal)

# =====================================================
# A* SEARCH
# =====================================================
def heuristic(a, b):
    x1, y1 = pos_state[a]
    x2, y2 = pos_state[b]
    return math.dist((x1, y1), (x2, y2))

def a_star_search(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {start: None}
    g_cost = {start: 0}
    edges = []

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        for nbr in graph[current]:
            tentative_g = g_cost[current] + 1
            if nbr not in g_cost or tentative_g < g_cost[nbr]:
                g_cost[nbr] = tentative_g
                f_cost = tentative_g + heuristic(nbr, goal)
                heapq.heappush(open_set, (f_cost, nbr))
                parent[nbr] = current
                edges.append((current, nbr))

    return edges, reconstruct_path(parent, start, goal)

# =====================================================
# RUN SEARCHES + TERMINAL OUTPUT
# =====================================================
dfs_edges, dfs_path = dfs_search(graph, start, goal)
bfs_edges, bfs_path = bfs_search(graph, start, goal)
astar_edges, astar_path = a_star_search(graph, start, goal)

print("\nDFS Final Path:")
print(" -> ".join(dfs_path))

print("\nBFS Final Path:")
print(" -> ".join(bfs_path))

print("\nA* Final Path:")
print(" -> ".join(astar_path))

# =====================================================
# VISUALIZATION 1: STATE SPACE GRAPH
# =====================================================
G = nx.Graph()
for n in graph:
    for nbr in graph[n]:
        G.add_edge(n, nbr)

plt.figure(figsize=(12,8))
nx.draw(
    G, pos_state,
    with_labels=True,
    node_color=["skyblue" if n == start else "red" if n == goal else "lightgray" for n in G.nodes()],
    node_size=1700,
    edgecolors="black"
)
plt.title("Visualization 1: State Space Graph (Map)", fontweight="bold")
plt.axis("off")
plt.show()

# =====================================================
# HELPER: TREE LAYOUT (LEVEL-WISE)
# =====================================================
def tree_layout(edges, root):
    levels = {root: 0}
    for u, v in edges:
        levels[v] = levels[u] + 1

    pos = {}
    x_offset = {}
    for node, lvl in levels.items():
        x_offset.setdefault(lvl, 0)
        pos[node] = (x_offset[lvl], -lvl)
        x_offset[lvl] += 1
    return pos

# =====================================================
# VISUALIZATION 2: DFS TREE
# =====================================================
DFS = nx.DiGraph(dfs_edges)
pos_dfs = tree_layout(dfs_edges, start)

plt.figure(figsize=(10,8))
nx.draw(DFS, pos_dfs, with_labels=True,
        node_color="lightyellow", node_size=1600,
        edgecolors="black", arrows=True)
plt.title("Visualization 2: DFS Search Tree", fontweight="bold")
plt.axis("off")
plt.show()

# =====================================================
# VISUALIZATION 3: BFS TREE
# =====================================================
BFS = nx.DiGraph(bfs_edges)
pos_bfs = tree_layout(bfs_edges, start)

plt.figure(figsize=(10,8))
nx.draw(BFS, pos_bfs, with_labels=True,
        node_color="lightgreen", node_size=1600,
        edgecolors="black", arrows=True)
plt.title("Visualization 3: BFS Search Tree", fontweight="bold")
plt.axis("off")
plt.show()

# =====================================================
# VISUALIZATION 4: A* SEARCH TREE (BONUS)
# =====================================================
ASTAR = nx.DiGraph(astar_edges)
pos_astar = tree_layout(astar_edges, start)

plt.figure(figsize=(10,8))
nx.draw(ASTAR, pos_astar, with_labels=True,
        node_color="lightblue", node_size=1600,
        edgecolors="black", arrows=True)
plt.title("Visualization 4: A* Search Tree (Heuristic Guided)", fontweight="bold")
plt.axis("off")
plt.show()
