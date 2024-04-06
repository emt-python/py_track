import time
import gc_count_module
import gc
import random
import sys
func = "obj_dump"

gc_count_module.start_count_gc_list(
    500_000, "/home/lyuze/workspace/py_track/1st.txt".format(func), 1, 21)
print("init + imported module", file=sys.stderr)
time.sleep(10)
gc_count_module.close_count_gc_list()
time.sleep(6)
print("moving forward", file=sys.stderr)
gc.collect()

matrix_size = 600
random.seed(1)
matrix_A = random.sample(range(3000, 400000), matrix_size * matrix_size)
matrix_A = [matrix_A[i:i+matrix_size]
            for i in range(0, len(matrix_A), matrix_size)]
# matrix_A = [[random.randint(1, 500) for _ in range(matrix_size)]
#             for _ in range(matrix_size)]
gc_count_module.start_count_gc_list(
    500_000, "/home/lyuze/workspace/py_track/2nd.txt".format(func), 1, 21)
print("matrix A created", file=sys.stderr)
time.sleep(10)
gc_count_module.close_count_gc_list()
time.sleep(6)
print("moving forward", file=sys.stderr)

matrix_B = random.sample(range(400000, 800000), matrix_size * matrix_size)
matrix_B = [matrix_B[i:i+matrix_size]
            for i in range(0, len(matrix_B), matrix_size)]
# matrix_B = [[random.randint(1, 500) for _ in range(matrix_size)]
#             for _ in range(matrix_size)]
gc_count_module.start_count_gc_list(
    500_000, "/home/lyuze/workspace/py_track/3rd.txt".format(func), 1, 21)
print("matrix B created", file=sys.stderr)
time.sleep(10)
gc_count_module.close_count_gc_list()
time.sleep(6)
