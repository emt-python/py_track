import networkx as nx
import random
import time
from collections import deque

def generate_large_graph(num_nodes, num_edges):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))


    while G.number_of_edges() < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
    
    return G


    #for i in range(num_nodes):
    #    for j in range(i + i, num_nodes):
    #        if random.random() > 0.5:
    #            G.add_edge(i, j, weight=random.randint(1, 10))

    #return G


def bfs_edges_from_source(G, source):
    bfs_tree_edges = list(nx.bfs_edges(G, source))
    return bfs_tree_edges


num_nodes = 10000
num_edges = 300000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
for i  in range(num_nodes):
    bfs_tree_edges = bfs_edges_from_source(G, i)
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")

