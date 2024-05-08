import networkx as nx
import random
import time
    
def generate_large_graph(num_nodes, num_edges):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))


    #for _ in range(num_edges):
    #    u = random.randint(0, num_nodes - 1)
    #    v = random.randint(0, num_nodes - 1)
    #    if u != v:
    #        G.add_edge(u, v)
    #
    #return G

    for i in range(num_nodes):
        for j in range(i + i, num_nodes):
            if random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))

    return G


def detect_communities_louvain(G):
    # Import the required community detection package from NetworkX
    from networkx.algorithms.community import louvain_communities

    # Detect communities using the Louvain method
    communities = louvain_communities(G)
    return communities

num_nodes = 5000
num_edges = 30000

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
for _ in range(5):
    communities = detect_communities_louvain(G)
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")

