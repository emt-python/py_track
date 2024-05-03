# import sys
# import math

# import math

import sys
import gc
import time


def doit_wo_list(x):
    y = 1
    x = [i*i for i in range(0, 80000000)][99999]
    y1 = [i*i for i in range(0, 80000000)][199999]
    z1 = [i for i in range(0, 8000000)][299999]
    z = x * y * y1 * z1
    return z


def doit_w_list(x):
    y = 1
    x_ = [i*i for i in range(0, 4000000)]
    x = x_[99999]
    y1_ = [i*i for i in range(0, 8200000)]
    y1 = y1_[199999]
    z1_ = [i for i in range(0, 6000000)]
    z1 = z1_[299999]
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
    for i in range(1, 2):
        print(i)
        for j in range(1, 10):
            x = doit_wo_list(x)
            # x = doit2(x)
            # x = doit3(x)
    return x


gc.collect()
# sys.setswitchinterval(1)
# gc.disable()
# sys.setswitchinterval(0.1)
start = time.time()
stuff()
print("Compute time: {:.2f}".format(time.time() - start))
