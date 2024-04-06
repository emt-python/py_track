# matmul.pyx

def matmul_cython(list A, list B):
    # Get dimensions
    a_rows = len(A)
    a_cols = len(A[0])
    b_rows = len(B)
    b_cols = len(B[0])

    # Check if multiplication is possible
    if a_cols != b_rows:
        raise ValueError("Matrices A and B cannot be multiplied")

    # Initialize the result matrix
    C = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

    # Perform matrix multiplication
    for i in range(a_rows):
        for j in range(b_cols):
            for k in range(a_cols):
                C[i][j] += A[i][k] * B[k][j]

    return C
