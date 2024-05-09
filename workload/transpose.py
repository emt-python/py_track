import random
import time
import gc_count_module

def matrix_transpose(A):
    """Transpose a matrix A."""
    n = len(A)
    m = len(A[0])
    # Initialize the transpose matrix T with zeros
    T = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            T[j][i] = A[i][j]
    return T


def generate_matrix(matrix_size):
    matrix_A = random.sample(range(
        matrix_size, matrix_size*matrix_size + matrix_size), matrix_size * matrix_size)
    matrix_A = [matrix_A[i:i+matrix_size]
                for i in range(0, len(matrix_A), matrix_size)]
    return matrix_A


# Define the size of the matrix (adjust these for larger/smaller matrices)
N = 8000  # Dimensions of the matrix (N x N)

# Generate two N x N matrices
start_time = time.time()
A = generate_matrix(N)
# B = generate_matrix(N)
end_time = time.time()
print("Generate Time: {:.2f} seconds".format(end_time - start_time))

# Measure time for matrix transpose
start_time = time.time()
gc_count_module.start_count_gc_list(
    250_000, "obj_dump.txt", 0, 7, 1_000_000)
T = matrix_transpose(A)
gc_count_module.close_count_gc_list()
end_time = time.time()
print("Matrix Transpose Time: {:.2f} seconds".format(end_time - start_time))
