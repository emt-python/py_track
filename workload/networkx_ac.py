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
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # for _ in range(num_edges):
    #    u = random.randint(0, num_nodes - 1)
    #    v = random.randint(0, num_nodes - 1)
    #    if u != v:
    #        G.add_edge(u, v)
    #
    # return G

    for i in range(num_nodes):
        for j in range(i + i, num_nodes):
            if random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))

    return G


def compute_average_clustering(G):
    # Calculate the average clustering coefficient
    avg_clustering = nx.average_clustering(G)
    return avg_clustering


num_nodes = 9000
num_edges = 30000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 7, 2_500_000)

average_clustering = compute_average_clustering(G)

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
