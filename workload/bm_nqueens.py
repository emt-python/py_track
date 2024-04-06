"""Simple, brute-force N-Queens solver."""
import time
__author__ = "collinwinter@google.com (Collin Winter)"
# import gc_count_module

# Pure-Python implementation of itertools.permutations().


def permutations(iterable, r=None):
    """permutations(range(3), 2) --> (0,1) (0,2) (1,0) (1,2) (2,0) (2,1)"""
    pool = tuple(iterable)
    n = len(pool)
    if r is None:
        r = n
    indices = list(range(n))
    cycles = list(range(n - r + 1, n + 1))[::-1]
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


# From http://code.activestate.com/recipes/576647/
def n_queens(queen_count):
    """N-Queens solver.

    Args:
        queen_count: the number of queens to solve for. This is also the
            board size.

    Yields:
        Solutions to the problem. Each yielded value is looks like
        (3, 8, 2, 1, 4, ..., 6) where each number is the column position for the
        queen, and the index into the tuple indicates the row.
    """
    cols = range(queen_count)
    for vec in permutations(cols):
        if (queen_count == len(set(vec[i] + i for i in cols))
                        == len(set(vec[i] - i for i in cols))):
            yield vec


def bench_n_queens(queen_count):
    list(n_queens(queen_count))


if __name__ == "__main__":

    queen_count = 11
    start = time.time()
    # gc_count_module.start_count_gc_list(
    #     250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 10, 1_000_000)
    bench_n_queens(queen_count)
    elapsed_time = time.time() - start
    # gc_count_module.close_count_gc_list()
    print(f"Compute time: {elapsed_time:.2f} seconds")
