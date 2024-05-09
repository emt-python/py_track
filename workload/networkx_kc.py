import networkx as nx
import random
import time
from networkx.algorithms import community
import gc_count_module


def generate_large_graph(num_nodes, num_edges):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    for _ in range(num_edges):
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            G.add_edge(u, v)

    return G

    # for i in range(num_nodes):
    #    for j in range(i + i, num_nodes):
    #        if random.random() > 0.5:
    #            G.add_edge(i, j, weight=random.randint(1, 10))

    # return G


def compute_k_core(G, k):
    # Compute the k-core of the graph
    k_core_graph = nx.k_core(G, k=k)
    return k_core_graph


num_nodes = 100000
num_edges = 10000000
k = 10

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
gc_count_module.start_count_gc_list(
    250_000, "obj_dump.txt", 0, 7, 2_500_000)
k_core_graph = compute_k_core(G, k)
gc_count_module.close_count_gc_list()
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
