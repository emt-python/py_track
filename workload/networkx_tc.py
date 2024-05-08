import networkx as nx
import random
import time
import gc_count_module


def generate_large_graph(num_nodes, num_edges):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(i + i, num_nodes):
            if random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))

    return G


def generate_large_graph_w_edges(num_nodes, num_edges):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # Calculate the maximum number of possible edges
    max_possible_edges = num_nodes * (num_nodes - 1) // 2

    if num_edges > max_possible_edges:
        raise ValueError("Too many edges! Maximum number of edges for {} nodes is {}.".format(
            num_nodes, max_possible_edges))

    # Generate a list of all possible edges
    all_possible_edges = [(i, j) for i in range(num_nodes)
                          for j in range(i+1, num_nodes)]

    # Randomly select num_edges from all possible edges
    selected_edges = random.sample(all_possible_edges, num_edges)

    # Add selected edges to the graph with random weights
    for edge in selected_edges:
        G.add_edge(edge[0], edge[1], weight=random.randint(1, 10))

    return G


def count_triangles(G):
    for i in range(1):
        triangles = sum(nx.triangles(G).values()) // 3
    return triangles


num_nodes = 6000
num_edges = 15000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
# gc_count_module.start_count_gc_list(
#     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 7, 1_000_000)
triangle_count = count_triangles(G)
compute_time = time.time() - start_comp
# gc_count_module.close_count_gc_list()
print(f"Compute time: {compute_time:.2f} seconds")

print(f"Total number of triangles: {triangle_count}")
