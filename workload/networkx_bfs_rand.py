import networkx as nx
import random
import time
from collections import deque
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


def generate_large_graph(num_nodes):
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + i, num_nodes):
            if random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))

    return G


def bfs_edges_from_source(G, source):
    bfs_tree_edges = list(nx.bfs_edges(G, source))
    return bfs_tree_edges


num_nodes = 12000
random.seed(42)

start_creating = time.time()
G = generate_large_graph(num_nodes)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds", file=sys.stderr)

start_comp = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)

for _ in range(3000):
    start_id = random.randint(0, 5000)
    bfs_tree_edges = bfs_edges_from_source(G, start_id)
    elapsed_time = time.time() - start_comp
    # if i % 100 == 0:
    #     print("computed to node", i, file=sys.stderr)
    #     print(f"Already compute time: {elapsed_time:.2f} seconds", file=sys.stderr)

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
