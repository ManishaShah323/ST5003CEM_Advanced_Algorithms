# =========================================================
# QUESTION 5(a): Interactive Emergency Network Simulator
# FINAL FULLY IMPROVED & EXAM-READY VERSION
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import networkx as nx
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class EmergencyNetworkSimulator:
    """
    Emergency Network Simulator
    ------------------------------------------------
    - Cities are represented as nodes
    - Roads are weighted edges
    - Supports:
        • Minimum Spanning Tree (Kruskal)
        • Shortest Path (Dijkstra)
        • Failure Simulation
        • Graph Coloring (Frequency Assignment)
        • Command Hierarchy Optimizer (BFS Tree)
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Emergency Network Simulator")
        self.root.geometry("1300x800")

        # Graph data
        self.G = nx.Graph()
        self.failed_nodes = set()
        self.pos = {}
        self.node_colors = {}

        # Status bar
        self.status = tk.StringVar(value="System Ready")

        self.setup_ui()
        self.initialize_network()

    # -------------------------------------------------
    # UI SETUP
    # -------------------------------------------------
    def setup_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        # Graph canvas
        self.fig = Figure(figsize=(8, 7))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=main)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control panel
        control = ttk.Frame(main, width=320)
        control.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        ttk.Label(control, text="Emergency Controls",
                  font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(control, text="Network Editing",
                  font=("Arial", 11, "bold")).pack(pady=5)

        ttk.Button(control, text="Create City", command=self.create_node).pack(fill=tk.X)
        ttk.Button(control, text="Delete City", command=self.delete_node).pack(fill=tk.X)

        ttk.Separator(control).pack(fill=tk.X, pady=5)

        ttk.Button(control, text="Add Road", command=self.add_road).pack(fill=tk.X)
        ttk.Button(control, text="Remove Road", command=self.remove_road).pack(fill=tk.X)

        ttk.Separator(control).pack(fill=tk.X, pady=5)

        ttk.Label(control, text="Analysis Tools",
                  font=("Arial", 11, "bold")).pack(pady=5)

        ttk.Button(control, text="Show MST (Kruskal)", command=self.show_mst).pack(fill=tk.X)
        ttk.Button(control, text="Reliable Path (Dijkstra)", command=self.reliable_path).pack(fill=tk.X)

        ttk.Separator(control).pack(fill=tk.X, pady=5)

        ttk.Button(control, text="Simulate Failure", command=self.simulate_failure).pack(fill=tk.X)
        ttk.Button(control, text="Assign Frequencies (Graph Coloring)", command=self.graph_coloring).pack(fill=tk.X)

        ttk.Separator(control).pack(fill=tk.X, pady=5)

        ttk.Button(control, text="Command Hierarchy Optimizer",
                   command=self.command_hierarchy_optimizer).pack(fill=tk.X)

        ttk.Button(control, text="Reset Network",
                   command=self.initialize_network).pack(fill=tk.X, pady=10)

        # Status bar
        ttk.Label(self.root, textvariable=self.status,
                  relief=tk.SUNKEN, anchor="w").pack(side=tk.BOTTOM, fill=tk.X)

    # -------------------------------------------------
    # INITIAL NETWORK
    # -------------------------------------------------
    def initialize_network(self):
        self.G.clear()
        self.failed_nodes.clear()
        self.node_colors.clear()

        edges = [
            ("HQ", "A", 4), ("HQ", "B", 6),
            ("A", "C", 3), ("B", "C", 2),
            ("C", "D", 5), ("D", "E", 7)
        ]
        self.G.add_weighted_edges_from(edges)

        self.pos = nx.spring_layout(self.G, seed=42)

        for node in self.G.nodes:
            self.node_colors[node] = "skyblue"

        self.draw_graph("Initial Emergency Network")
        self.status.set("Network initialized")

    # -------------------------------------------------
    # ACTIVE GRAPH
    # -------------------------------------------------
    def active_graph(self):
        H = self.G.copy()
        H.remove_nodes_from(self.failed_nodes)
        return H

    # -------------------------------------------------
    # DRAW GRAPH
    # -------------------------------------------------
    def draw_graph(self, title, highlight_edges=None, info_text=None):
        self.ax.clear()

        colors = [
            "red" if n in self.failed_nodes else self.node_colors.get(n, "skyblue")
            for n in self.G.nodes
        ]

        nx.draw(self.G, self.pos, ax=self.ax,
                with_labels=True,
                node_color=colors,
                node_size=1200,
                edge_color="gray")

        nx.draw_networkx_edge_labels(
            self.G, self.pos,
            edge_labels=nx.get_edge_attributes(self.G, "weight"),
            ax=self.ax
        )

        if highlight_edges:
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=highlight_edges,
                edge_color="green",
                width=4,
                ax=self.ax
            )

        legend = (
            "Legend:\n"
            "Blue : Active City\n"
            "Red  : Failed City\n"
            "Green Edge : Path / Tree / MST"
        )

        if info_text:
            legend += f"\n\n{info_text}"

        self.ax.text(
            0.01, 0.01, legend,
            transform=self.ax.transAxes,
            fontsize=9,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
        )

        self.ax.set_title(title)
        self.canvas.draw()

    # -------------------------------------------------
    # CREATE NODE
    # -------------------------------------------------
    def create_node(self):
        node = simpledialog.askstring("Create City", "Enter city name:")
        if not node or node in self.G:
            messagebox.showerror("Error", "Invalid or duplicate city.")
            return

        self.G.add_node(node)
        self.pos[node] = (random.uniform(-1, 1), random.uniform(-1, 1))
        self.node_colors[node] = "skyblue"

        if len(self.G.nodes) > 1:
            other = random.choice([n for n in self.G.nodes if n != node])
            self.G.add_edge(node, other, weight=random.randint(1, 10))

        self.draw_graph(f"City {node} Added")
        self.status.set(f"City '{node}' created")

    # -------------------------------------------------
    # DELETE NODE
    # -------------------------------------------------
    def delete_node(self):
        node = simpledialog.askstring("Delete City", "Enter city name:")
        if node not in self.G:
            messagebox.showerror("Error", "City not found.")
            return

        self.G.remove_node(node)
        self.pos.pop(node, None)
        self.node_colors.pop(node, None)
        self.failed_nodes.discard(node)

        self.draw_graph(f"City {node} Deleted")
        self.status.set(f"City '{node}' deleted")

    # -------------------------------------------------
    # ADD ROAD
    # -------------------------------------------------
    def add_road(self):
        u = simpledialog.askstring("Add Road", "Source city:")
        v = simpledialog.askstring("Add Road", "Destination city:")
        w = simpledialog.askinteger("Add Road", "Road weight:")

        if not u or not v or w is None:
            return
        if u not in self.G or v not in self.G:
            messagebox.showerror("Error", "Both cities must exist.")
            return

        self.G.add_edge(u, v, weight=w)
        self.draw_graph(f"Road Added: {u} ↔ {v}")
        self.status.set("Road added successfully")

    # -------------------------------------------------
    # REMOVE ROAD
    # -------------------------------------------------
    def remove_road(self):
        u = simpledialog.askstring("Remove Road", "Source city:")
        v = simpledialog.askstring("Remove Road", "Destination city:")

        if not self.G.has_edge(u, v):
            messagebox.showerror("Error", "Road does not exist.")
            return

        self.G.remove_edge(u, v)
        self.draw_graph(f"Road Removed: {u} ↔ {v}")
        self.status.set("Road removed")

    # -------------------------------------------------
    # MST – KRUSKAL
    # -------------------------------------------------
    def show_mst(self):
        H = self.active_graph()
        if H.number_of_nodes() < 2:
            messagebox.showwarning("Error", "Not enough active cities.")
            return

        mst = nx.minimum_spanning_tree(H, algorithm="kruskal")
        cost = sum(d["weight"] for _, _, d in mst.edges(data=True))

        messagebox.showinfo(
            "Kruskal's Algorithm",
            "Builds the Minimum Spanning Tree by\n"
            "adding the smallest edges without cycles.\n\n"
            "Time Complexity: O(E log E)"
        )

        self.draw_graph(
            "Minimum Spanning Tree (Kruskal)",
            list(mst.edges()),
            info_text=f"MST Total Cost = {cost}"
        )

        self.status.set("MST generated using Kruskal")

    # -------------------------------------------------
    # DIJKSTRA SHORTEST PATH
    # -------------------------------------------------
    def reliable_path(self):
        H = self.active_graph()
        nodes = list(H.nodes)

        src = simpledialog.askstring("Source", f"Choose from {nodes}")
        dst = simpledialog.askstring("Destination", f"Choose from {nodes}")

        if src not in nodes or dst not in nodes:
            messagebox.showerror("Error", "Invalid city selection.")
            return

        try:
            path = nx.shortest_path(H, src, dst, weight="weight")
            cost = nx.shortest_path_length(H, src, dst, weight="weight")
        except nx.NetworkXNoPath:
            messagebox.showwarning("No Path", "No reliable path exists.")
            return

        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        messagebox.showinfo(
            "Dijkstra's Algorithm",
            "Finds the shortest path by expanding\n"
            "the closest unvisited node.\n\n"
            "Time Complexity: O(E log V)"
        )

        self.draw_graph(
            "Reliable Path (Dijkstra)",
            edges,
            info_text=f"Path Cost = {cost}"
        )

        self.status.set(f"Shortest path from {src} to {dst}")

    # -------------------------------------------------
    # FAILURE SIMULATION
    # -------------------------------------------------
    def simulate_failure(self):
        node = simpledialog.askstring("Failure", "Enter city to disable:")
        if node not in self.G:
            messagebox.showerror("Error", "City not found.")
            return

        self.failed_nodes.add(node)
        self.draw_graph(f"City {node} Failed")
        self.status.set(f"Failure simulated at {node}")

    # -------------------------------------------------
    # GRAPH COLORING
    # -------------------------------------------------
    def graph_coloring(self):
        coloring = nx.coloring.greedy_color(self.G, strategy="largest_first")
        palette = ["red", "green", "yellow", "orange", "purple"]

        for node, color in coloring.items():
            self.node_colors[node] = palette[color % len(palette)]

        self.draw_graph("Frequency Assignment (Graph Coloring)")
        self.status.set("Frequencies assigned")

    # -------------------------------------------------
    # COMMAND HIERARCHY OPTIMIZER (BFS)
    # -------------------------------------------------
    def command_hierarchy_optimizer(self):
        H = self.active_graph()

        if "HQ" not in H.nodes:
            messagebox.showerror("Error", "HQ must exist for command hierarchy.")
            return

        tree = nx.bfs_tree(H, source="HQ")
        edges = list(tree.edges())

        messagebox.showinfo(
            "Command Hierarchy Optimizer",
            "Optimizes command dissemination using\n"
            "Breadth-First Search (BFS).\n\n"
            "Ensures minimum communication depth.\n"
            "Time Complexity: O(V + E)"
        )

        self.draw_graph(
            "Optimized Command Hierarchy (BFS Tree)",
            highlight_edges=edges,
            info_text="Root Node: HQ\nStrategy: BFS Hierarchy"
        )

        self.status.set("Command hierarchy optimized")


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    EmergencyNetworkSimulator(root)
    root.mainloop()
