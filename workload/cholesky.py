import gc
import sys
import random
from math import sqrt, isclose
import time
import gc_count_module


def cholesky(A):
    """Performs a Cholesky decomposition of A, which must
    be a symmetric and positive definite matrix. The function
    returns the lower variant triangular matrix, L."""
    n = len(A)

    # Create zero matrix for L
    L = [[0.0] * n for i in range(n)]

    # Perform the Cholesky decomposition
    for i in range(n):
        for k in range(i + 1):
            tmp_sum = sum(L[i][j] * L[k][j] for j in range(k))

            if i == k:  # Diagonal elements
                # Ensure that the value inside the sqrt is non-negative
                # if A[i][i] - tmp_sum < 0:
                #     raise ValueError("Matrix is not positive definite")
                L[i][k] = sqrt(A[i][i] - tmp_sum)
            else:
                # if L[k][k] == 0:
                #     raise ValueError("Division by zero")
                L[i][k] = (1.0 / L[k][k]) * (A[i][k] - tmp_sum)
    return L


def partial_cholesky(A, percentage=25):
    """Performs a partial Cholesky decomposition of A, which must
    be a symmetric and positive definite matrix. The function
    computes only a percentage of the matrix and returns the
    lower variant triangular matrix, L."""
    n = len(A)
    # Calculate boundary for partial computation
    p = int((percentage / 100.0) * n)

    # Create zero matrix for L
    L = [[0.0] * n for _ in range(n)]

    # Perform the partial Cholesky decomposition
    for i in range(p):  # Only go up to p to compute a percentage of the matrix
        for k in range(i + 1):
            tmp_sum = sum(L[i][j] * L[k][j] for j in range(k))

            if i == k:  # Diagonal elements
                if A[i][i] - tmp_sum <= 0:
                    raise ValueError("Matrix is not positive definite")
                L[i][k] = sqrt(A[i][i] - tmp_sum)
            else:
                if L[k][k] == 0:
                    raise ValueError("Division by zero")
                L[i][k] = (1.0 / L[k][k]) * (A[i][k] - tmp_sum)
    return L


def generate_large_symmetric_pd_matrix(n):
    """Generates a large symmetric and positive definite matrix of size n x n."""
    # A = [[random.random() for _ in range(n)] for _ in range(n)]
    # start = time.time()
    A = random.sample(range(1, n*n+1000), n * n)
    # end1 = time.time()
    # print("time1", end1-start, file=sys.stderr)
    A = [A[i:i+n]
         for i in range(0, len(A), n)]
    # end2 = time.time()
    # print("time2", end2-end1, file=sys.stderr)
    for i in range(n):
        for j in range(i + 1, n):
            A[j][i] = A[i][j]
    # end3 = time.time()
    # print("time3", end3-end2, file=sys.stderr)
    for i in range(n):
        A[i][i] = sum(abs(A[i][j]) for j in range(n)) + 1
    # end4 = time.time()
    # print("time4", end4-end3, file=sys.stderr)
    return A


gc.disable()


def generate_modified_matrix(n):
    """Generates a modified matrix with different computations on each quadrant."""
    # Initialize matrix with random values
    # A = [[random.randint(1, n * n + 1000) for _ in range(n)] for _ in range(n)]
    A = random.sample(range(1, n*n+1000), n * n)

    quarter = n // 4  # Calculate quarter of the matrix size

    # First part: Copy upper triangle to lower triangle in the first quadrant
    for i in range(quarter):
        for j in range(i + 1, quarter):
            A[j][i] = A[i][j]

    # Second part: Reverse traverse and copy lower triangle to upper in the second quadrant
    for i in range(quarter, 2 * quarter):
        for j in range(i + 1, 2 * quarter):
            A[i][j] = A[j][i]

    # Third part: Assign random values to the lower triangle in the third quadrant
    # for i in range(2 * quarter, 3 * quarter):
    #     for j in range(i + 1, 3 * quarter):
    #         A[j][i] = random.randint(1, n * n + 1000)

    # # Fourth part: Set each element to the sum of its current row values in the fourth quadrant
    # for i in range(3 * quarter, n):
    #     row_sum = sum(A[i][j] for j in range(n))
    #     for j in range(3 * quarter, n):
    #         A[i][j] = row_sum

    # # Make the whole matrix symmetric
    # for i in range(n):
    #     for j in range(i + 1, n):
    #         A[j][i] = A[i][j]

    # Make sure diagonal is dominant to keep matrix positive definite
    for i in range(n):
        A[i][i] = sum(abs(A[i][j]) for j in range(n)) + 1

    return A


start_creating = time.time()
n = 6000
# gc_count_module.start_count_gc_list(
#     250_000, "obj_dump.txt", 0, 7, 1_000_000)
A = generate_large_symmetric_pd_matrix(n)
# gc_count_module.close_count_gc_list()
# A = generate_modified_matrix(n)
creation_time = time.time() - start_creating
print(f"Creation_time: {creation_time:.2f} seconds", file=sys.stderr)

# start_comp = time.time()
# # L = cholesky(A)
# L = partial_cholesky(A, 25)
# compute_time = time.time() - start_comp
# print(f"Compute time: {compute_time:.2f} seconds", file=sys.stderr)
