#!/usr/bin/env python3
import gc
import sys
import time
import gc_count_module
sys.setswitchinterval(0.0001)
gc.collect()
gc.disable()
# import math

# from numpy import linalg as LA

# arr = [i for i in range(400000, 401000)]


def doit1(x):
    y = 1
    x = [i*i for i in range(400000, 2000000)][99999]
    y1 = [i*i for i in range(1000000, 2000000)][199999]
    z1 = [i for i in range(1500000, 2000000)][299999]
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


def dummy():
    time.sleep(20)


print("TESTME")
print(sys.argv)
start = time.time()
gc_count_module.start_count_gc_list(
    250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 1, 5, 3500000)
stuff()
# dummy()
gc_count_module.close_count_gc_list()
latency = time.time() - start
print("latency: {:.3f} seconds".format(latency), file=sys.stderr)
