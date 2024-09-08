import time
import networkx as nx
import random
import os
import sys
is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

if sys.argv[1] == "no_gc":
    print("running no gc")
    import gc
    gc.disable()
elif sys.argv[1] == "with_gc":
    print("running with gc")
else:
    print("Using GC or not? Forget to specify?")

enable_tracing = False
if len(sys.argv) != 2:
    print("enable tracing")
    enable_tracing = True


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


def compute_astar(G):
    # Increase memory usage by enlarging the working data set
    # Replicate nodes to artificially increase processing
    nodes = list(G.nodes())
    # stored_paths = {}

    # for idx in range(num_pairs):
    #     u, v = random.sample(nodes, 2)
    #     path = nx.shortest_path(G, source=u, target=v, weight='weight')

    # Store each path with a unique key to prevent overwriting
    # stored_paths[(u, v)] = path

    for _ in range(20):  # Artificially add computation steps
        u, v = random.sample(nodes, 2)
        _ = nx.astar_path(G, source=u, target=v, weight='weight')

    # Further increase memory usage by duplicating the stored paths dictionary
    # duplicated_paths = {key: value for key, value in stored_paths.items()}

    # return duplicated_paths


# 6000: 3216 MB
if __name__ == "__main__":
    num_nodes = 9000  # should be 9000
    # G = nx.gnp_random_graph(10000, 0.5, seed=42, directed=True)
    # nx.set_edge_attributes(G, {e: random.randint(1, 10)
    #                        for e in G.edges()}, 'weight')
    start_creating = time.time()
    G = create_large_dense_graph(num_nodes)
    # G = create_large_dense_graph_with_edges(num_nodes, num_edges)
    creation_time = time.time() - start_creating
    print(f"Creation time: {creation_time:.2f} seconds", file=sys.stderr)

    start_comp = time.time()
    if is_pypper and enable_tracing:
        gc_count_module.start_count_gc_list(
            250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)
    compute_astar(G)
    if is_pypper and enable_tracing:
        gc_count_module.close_count_gc_list()
    compute_time = time.time() - start_comp
    print(f"Compute time: {compute_time:.2f} seconds", file=sys.stderr)
