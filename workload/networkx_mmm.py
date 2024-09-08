import networkx as nx
import random
import time
import networkx.algorithms.approximation as naa
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
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + i, num_nodes):
            if random.random() > 0.5:
                G.add_edge(i, j, weight=random.randint(1, 10))

    return G


def compute_min_maximal_matching(G):
    matching = naa.min_maximal_matching(G)
    return matching


num_nodes = 13000

start_creating = time.time()
G = generate_large_graph(num_nodes)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds")

start_comp = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)

for _ in range(10):
    matching = compute_min_maximal_matching(G)

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
compute_time = time.time() - start_comp
print(f"Compute time: {compute_time:.2f} seconds")
