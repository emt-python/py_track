import threading
import time

# Define a function for the thread


def print_message(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(f"{thread_name}: {time.ctime(time.time())}")


# Create two threads
thread1 = threading.Thread(target=print_message, args=("Thread-1", 1))
thread2 = threading.Thread(target=print_message, args=("Thread-2", 2))

# Start the threads
thread1.start()
thread2.start()

# Wait for all threads to complete
thread1.join()
thread2.join()

print("Exiting Main Thread")
