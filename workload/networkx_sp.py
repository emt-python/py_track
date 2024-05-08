import time
import networkx as nx
import random
import gc_count_module


def create_large_dense_graph(num_nodes):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            # Adding an edge with a random weight
            if random.random() > 0.5:  # Adjust density with probability condition
                G.add_edge(i, j, weight=random.randint(1, 10))
    return G


def create_large_dense_graph_with_edges(num_nodes, num_edges=1000):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    possible_edges = [(i, j) for i in range(num_nodes)
                      for j in range(i+1, num_nodes)]
    random.shuffle(possible_edges)

    edges_added = 0
    while edges_added < num_edges and possible_edges:
        edge = possible_edges.pop()
        weight = random.randint(1, 10)  # Generate a random weight
        G.add_edge(edge[0], edge[1], weight=weight)
        edges_added += 1
    if edges_added < num_edges:
        raise ValueError(
            "The number of edges requested exceeds the number of possible edges between nodes.")
    return G


def compute_shortest_paths(G, num_pairs=10):
    # Increase memory usage by enlarging the working data set
    # Replicate nodes to artificially increase processing
    nodes = list(G.nodes()) * 10
    stored_paths = {}

    for _ in range(num_pairs * 10):
        u, v = random.sample(nodes, 2)
        path = nx.shortest_path(G, source=u, target=v, weight='weight')

        # Store each path with a unique key to prevent overwriting
        stored_paths[(u, v)] = path

        # Redundant computation for memory traffic
        for _ in range(5):  # Artificially add computation steps
            _ = nx.shortest_path(G, source=u, target=v, weight='weight')

    # Further increase memory usage by duplicating the stored paths dictionary
    duplicated_paths = {key: value for key, value in stored_paths.items()}

    return duplicated_paths


# 6000: 3216 MB
if __name__ == "__main__":
    start_creating = time.time()
    num_nodes = 9000
    num_edges = 1000
    # G = nx.gnp_random_graph(10000, 0.5, seed=42, directed=True)
    # nx.set_edge_attributes(G, {e: random.randint(1, 10)
    #                        for e in G.edges()}, 'weight')
    G = create_large_dense_graph(num_nodes)
    # G = create_large_dense_graph_with_edges(num_nodes, num_edges)
    creation_time = time.time() - start_creating
    print(f"Creation time: {creation_time:.2f} seconds")

    # gc_count_module.start_count_gc_list(
    #     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 6, 10_000_000)
    start_comp = time.time()
    compute_shortest_paths(G, num_pairs=10)
    compute_time = time.time() - start_comp
    # gc_count_module.close_count_gc_list()
    print(f"Compute time: {compute_time:.2f} seconds")
