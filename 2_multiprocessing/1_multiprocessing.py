import time
from multiprocessing import Process, Queue
import os

tasks = [(5, 4), (10, 1), (8, 3), (11, 1), (20, 2), (18, 1), (100, 2), (15, 2)]
# sum = 187

results = []


# we are using queue for inter-process communications
def retrieve_value(task, queue):
    value, delay = task
    time.sleep(delay)
    queue.put(value)
    return value


def sum_tasks(tasks):
    queue = Queue()
    threads = []
    sum = 0

    for task in tasks:
        thread = Process(target=retrieve_value, args=(task, queue))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    while not queue.empty():
        sum += queue.get()

    return sum


def run_tasks():
    start = time.perf_counter()
    print('sum', sum_tasks(tasks))

    end = time.perf_counter()

    print(f'ran for {end - start:.2f} seconds')


if __name__ == '__main__':
    run_tasks()
    print(os.cpu_count())

# processes can be terminated, process.terminate()
# although, through this approach, shared resources may be left in unstable state. exit handlers arent run too.
