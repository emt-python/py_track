# import sys
# import math

# import math

# from numpy import linalg as LA
# import gc_count_module
import gc
import time


def doit1(x):
    y = 1
    x = [i*i for i in range(0, 4000000)][99999]
    y1 = [i*i for i in range(0, 8200000)][199999]
    z1 = [i for i in range(0, 6000000)][299999]
    z = x * y * y1 * z1
    return z


def doit2(x):
    i = 0
    z = 0.1
    while i < 600000:
        z = z * z + z * x
        i += 1
    return z


def doit3(x):
    z = x + 1
    for _ in range(100):
        z = x + z
    return z


def stuff():
    x = 1.01
    for i in range(1, 5):
        print(i)
        for j in range(1, 10):
            x = doit1(x)
            # x = doit2(x)
            # x = doit3(x)
    return x


gc.collect()
# gc_count_module.start_count_gc_list(
#     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 10, 1_000_000)
start = time.time()
stuff()
print("latency: {:.2f}".format(time.time() - start))
# gc_count_module.close_count_gc_list()
