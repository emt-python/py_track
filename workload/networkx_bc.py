import networkx as nx
import random
import time
import os
import sys

is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

enable_tracing = False
if len(sys.argv) != 1:
    print("enable tracing")
    enable_tracing = True


def generate_large_graph(num_nodes, num_edges):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))

    # while G.number_of_edges() < num_edges:
    #    u = random.randint(0, num_nodes - 1)
    #    v = random.randint(0, num_nodes - 1)
    #    if u != v and not G.has_edge(u, v):
    #        G.add_edge(u, v)
    #
    # return G

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


def compute_betweenness_centrality(G):
    centrality = nx.betweenness_centrality(G)
    return centrality


num_nodes = 7000
num_edges = 300000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)
for _ in range(1):
    centrality = compute_betweenness_centrality(G)
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
