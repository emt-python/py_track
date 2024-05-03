import networkx as nx
import random
import time

def generate_large_graph(num_nodes, num_edges):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))
    
    #while G.number_of_edges() < num_edges:
    #    u = random.randint(0, num_nodes - 1)
    #    v = random.randint(0, num_nodes - 1)
    #    if u != v and not G.has_edge(u, v):
    #        G.add_edge(u, v)
    #
    #return G

    for i in range(num_nodes):
        for j in range(i + i, num_nodes):
            if random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))

    return G

def compute_pagerank(G):
    pagerank = nx.pagerank(G, alpha=0.85)
    return pagerank


num_nodes = 10000  
num_edges = 300000 

start_creating = time.time()
G = generate_large_graph(num_nodes, num_edges)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
for _ in range(1):
    pagerank = compute_pagerank(G)
    #for _ in range(1):
    #    compute_pagerank(G)
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")


for node_id, rank in list(pagerank.items())[:10]:
    print(f"Node {node_id}: PageRank {rank}")
