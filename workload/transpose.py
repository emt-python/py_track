import random
import time
import sys
import os
# import gc_count_module

is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

enable_tracing = False
if len(sys.argv) != 1:
    print("enable tracing")
    enable_tracing = True


def matrix_transpose(A):
    # """Transpose a matrix A."""
    n = len(A)
    m = len(A[0])
    T = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            time.sleep(0.00001)
            T[j][i] = A[i][j]
    return T
    # return [list(row) for row in zip(*A) if not time.sleep(0.0001)]


def generate_matrix(matrix_size):
    matrix_A = random.sample(range(
        matrix_size, matrix_size*matrix_size + matrix_size), matrix_size * matrix_size)
    matrix_A = [matrix_A[i:i+matrix_size]
                for i in range(0, len(matrix_A), matrix_size)]
    return matrix_A


# Define the size of the matrix (adjust these for larger/smaller matrices)
N = 1000  # Dimensions of the matrix (N x N)

# Generate two N x N matrices
start_time = time.time()
A = generate_matrix(N)
# B = generate_matrix(N)
end_time = time.time()
print("Generate Time: {:.2f} seconds".format(end_time - start_time))

# Measure time for matrix transpose
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        100_000, "obj_dump.txt", 1, 1024, 1_000_000, 5)
start_time = time.time()
T = matrix_transpose(A)
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()

end_time = time.time()
print("Matrix Transpose Time: {:.2f} seconds".format(end_time - start_time))
