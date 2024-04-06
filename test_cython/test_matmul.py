from matmul import matmul_cython
import random
import time
import gc
gc.collect()
matrix_size = 600
random.seed(1)
matrix_A = random.sample(range(3000, 400000), matrix_size * matrix_size)
matrix_A = [matrix_A[i:i+matrix_size]
            for i in range(0, len(matrix_A), matrix_size)]
matrix_B = random.sample(range(400000, 800000), matrix_size * matrix_size)
matrix_B = [matrix_B[i:i+matrix_size]
            for i in range(0, len(matrix_B), matrix_size)]

# matrix_A = random.sample(range(3000, 400000), matrix_size * matrix_size)
# matrix_A = [matrix_A[i:i+matrix_size]
#             for i in range(0, len(matrix_A), matrix_size)]
# matrix_B = random.sample(range(400000, 800000), matrix_size * matrix_size)
# matrix_B = [matrix_B[i:i+matrix_size]
#             for i in range(0, len(matrix_B), matrix_size)]

# result = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

start = time.time()
C = matmul_cython(matrix_A, matrix_B)
latency = time.time() - start
print("latency: {:.3f} for {}*{}".format(latency, matrix_size, matrix_size))
