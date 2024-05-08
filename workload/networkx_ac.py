import networkx as nx
import random
import time


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


num_nodes = 3000
num_edges = 30000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
average_clustering = compute_average_clustering(G)
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
