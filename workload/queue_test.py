import secrets
from queue import Queue
from threading import Thread


class QueueConsumer(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        while True:
            item = self.queue.get()
            if item is None:
                # Signal to terminate
                break  # Exit the loop to end this consumer thread
            # Process item here (omitted for brevity)
            self.queue.task_done()


class QueueProducer(Thread):
    def __init__(self, count, payload, queue):
        super().__init__()
        self.count = count
        self.payload = payload
        self.queue = queue

    def run(self) -> None:
        for _ in range(self.count):
            self.queue.put(self.payload)
        self.queue.join()  # Wait for the queue to be empty


class QueueBenchmark:
    def __init__(self):
        self.size = 10240000  # Reduced size for demonstration
        self.count = 1000
        self.prods = 2000  # Number of producer threads
        self.cons = 2000  # Number of consumer threads
        self.payload = secrets.token_bytes(self.size)
        self.queue = Queue(maxsize=20)

    def task(self) -> None:
        # Start producer threads
        producers = [QueueProducer(self.count, self.payload, self.queue)
                     for _ in range(self.prods)]
        for producer in producers:
            producer.start()

        # Start consumer threads
        consumers = [QueueConsumer(self.queue) for _ in range(self.cons)]
        for consumer in consumers:
            consumer.start()

        # Wait for all producers to finish
        for producer in producers:
            producer.join()

        # Signal consumers to stop by adding one sentinel per consumer
        for _ in range(self.cons):
            self.queue.put(None)

        # Wait for all consumers to finish
        for consumer in consumers:
            consumer.join()

        print("Queue Benchmark completed.")


# Example usage
if __name__ == "__main__":
    benchmark = QueueBenchmark()
    benchmark.task()
