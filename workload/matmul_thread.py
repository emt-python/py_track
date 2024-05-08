import random
import threading
import time
import sys
import gc_count_module

matrix_size = 600
matrix_A = random.sample(range(30000, 5000000), matrix_size * matrix_size)
matrix_A = [matrix_A[i:i+matrix_size]
            for i in range(0, len(matrix_A), matrix_size)]
matrix_B = random.sample(range(5000000, 9400000), matrix_size * matrix_size)
matrix_B = [matrix_B[i:i+matrix_size]
            for i in range(0, len(matrix_B), matrix_size)]
result = [[0] * matrix_size for _ in range(matrix_size)]


def matrix_multiply_task(start, end):
    for i in range(start, end):
        for j in range(matrix_size):
            for k in range(matrix_size):
                result[i][j] += matrix_A[i][k] * matrix_B[k][j]


num_threads = 4
threads = []
chunk_size = matrix_size // num_threads

for i in range(num_threads):
    start = i * chunk_size
    end = start + chunk_size if i < num_threads - 1 else matrix_size
    thread = threading.Thread(target=matrix_multiply_task, args=(start, end))
    threads.append(thread)
    thread.start()

start = time.time()
# gc_count_module.start_count_gc_list(
# 500_000, "obj_dump.txt", 0, 6, 1_000_000)
for thread in threads:
    thread.join()

latency = time.time() - start
# gc_count_module.close_count_gc_list()
print("latency: {:.3f} for {}*{}".format(latency,
                                         matrix_size, matrix_size), file=sys.stderr)
