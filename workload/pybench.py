import gc_count_module
import time
import argparse
import secrets
from threading import Thread
from queue import Queue
import numpy as np


class Iter:
    def __init__(self):
        self.size = int(float(500000000))  # Default size

    def task(self) -> None:
        for _ in range(self.size):
            pass
        print("Iter completed.")


class MapReduce:
    def __init__(self):
        self.size = int(float(30000000))  # Default size for MapReduce
        self.data = (list(np.random.rand(self.size)),
                     list(np.random.rand(self.size)))

    def task(self) -> None:
        result = sum(map(
            lambda pair: pair[0] * pair[1], filter(lambda pair: pair[0] > pair[1], zip(*self.data))))
        print(f"MapReduce Result: {result}")


def _fibonacci_impl(n: int) -> int:
    if n <= 1:
        return n
    else:
        return _fibonacci_impl(n - 1) + _fibonacci_impl(n - 2)


class Fibonacci:
    def __init__(self):
        self.size = int(float(37))  # Default size for Fibonacci

    def task(self) -> None:
        result = _fibonacci_impl(self.size)
        print(f"Fibonacci Result: {result}")


class QueueBenchmark:
    def __init__(self):
        self.size = 10240000
        self.count = 4000
        self.prods = 2000
        self.cons = 2000
        self.payload = secrets.token_bytes(self.size)
        self.queue = Queue(maxsize=2*self.cons)
        self.consumers = [QueueConsumer(self.queue) for _ in range(self.cons)]
        self.producers = [QueueProducer(
            self.count, self.payload, self.queue) for _ in range(self.prods)]

    def task(self) -> None:
        for producer in self.producers:
            producer.start()
        for consumer in self.consumers:
            consumer.start()
        for producer in self.producers:
            producer.join()
        for _ in self.consumers:
            self.queue.put(None)
        for consumer in self.consumers:
            consumer.join()
        print("Queue Benchmark completed.")


class QueueConsumer(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        while self.queue.get() is not None:
            pass


class QueueProducer(Thread):
    def __init__(self, count, payload, queue):
        super().__init__()
        self.count = count
        self.payload = payload
        self.queue = queue

    def run(self) -> None:
        for _ in range(self.count):
            self.queue.put(self.payload)


def main():
    parser = argparse.ArgumentParser(
        description="Run different Python benchmarks.")
    parser.add_argument(
        'benchmark', help='The benchmark to run (iter, mapreduce, fibonacci, queue)')
    args = parser.parse_args()

    if args.benchmark == 'iter':
        task = Iter()
    elif args.benchmark == 'mapreduce':
        task = MapReduce()
    elif args.benchmark == 'fibonacci':
        task = Fibonacci()
    elif args.benchmark == 'queue':
        task = QueueBenchmark()
    else:
        raise ValueError("Unknown benchmark requested.")

    gc_count_module.start_count_gc_list(
        250_000, "/home/lyuze/workspace/py_track/obj_dump.txt", 1, 10, 1_000_000)
    start_time = time.time()
    task.task()
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
    gc_count_module.close_count_gc_list()


if __name__ == "__main__":
    main()
