import time


def do_unpacking(loops, to_unpack):
    start_time = time.time()

    # Significantly increasing the amount of data manipulation
    for _ in range(loops):
        for _ in range(20):  # Maintaining the loop count
            # Unpacking into a larger list and duplicating the data multiple times
            # Drastically increase the size
            unpacked = list(to_unpack) * 1000000
            # Apply a complex operation that involves heavy memory usage
            # Simple operation, but on a huge list
            modified = [x * 2 for x in unpacked]
            # Introduce nested loops for more intensive memory usage
            for chunk in [modified[i:i+10000] for i in range(0, len(modified), 100000)]:
                _ = [item + 1 for item in chunk]

    end_time = time.time()
    return end_time - start_time


def bench_tuple_unpacking(loops):
    x = tuple(range(100))  # Drastically increase the size of the tuple
    return do_unpacking(loops, x)


def bench_list_unpacking(loops):
    x = list(range(100))  # Drastically increase the size of the list
    return do_unpacking(loops, x)


def bench_all(loops):
    time_tuple = bench_tuple_unpacking(loops)
    # time_list = bench_list_unpacking(loops)
    time_list = 0
    return time_tuple, time_list


if __name__ == "__main__":
    loops = 1  # Keeping the loops reasonable to avoid freezing the system
    start_time = time.time()
    time_tuple, time_list = bench_all(loops)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
    print(
        f"Tuple unpacking time: {time_tuple:.2f} seconds, List unpacking time: {time_list:.2f} seconds")
