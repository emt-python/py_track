import gc
import time
import gc_count_module


class Node:
    def __init__(self):
        self.ref = None


def create_cycles(num):
    for _ in range(num):
        a = Node()
        b = Node()
        a.ref = b
        b.ref = a


def main():
    gc.enable()  # Make sure garbage collection is enabled
    gc_count_module.start_count_gc_list(
        200_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 0, 21, 250000)
    while True:
        create_cycles(1000)
        gc.collect()  # Manually trigger garbage collection
        time.sleep(0.01)
    gc_count_module.close_count_gc_list()


if __name__ == "__main__":
    main()
