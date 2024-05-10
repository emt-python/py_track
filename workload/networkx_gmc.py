import networkx as nx
import random
import time
from networkx.algorithms import community
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

    cluster_size = num_nodes // 10  # Assume 10 clusters
    for i in range(10):
        # Each cluster is a smaller subgraph
        start = i * cluster_size
        end = start + cluster_size
        # Fully connect the nodes within this cluster
        for u in range(start, end):
            for v in range(u + 1, end):
                G.add_edge(u, v)

    additional_edges = num_edges - G.number_of_edges()
    while additional_edges > 0:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
            additional_edges -= 1

    return G

    # for i in range(num_nodes):
    #    for j in range(i + i, num_nodes):
    #        if random.random() > 0.5:
    #            G.add_edge(i, j, weight=random.randint(1, 10))

    # return G


def bfs_edges_from_source(G, source):
    bfs_tree_edges = list(nx.bfs_edges(G, source))
    return bfs_tree_edges


num_nodes = 15000
num_edges = 300000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")


def detect_communities(G):
    communities = community.greedy_modularity_communities(G)
    return communities


start_comp = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 7, 2_500_000)
communities = detect_communities(G)

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
