import time
from threading import Thread

tasks = [(5, 4), (10, 1), (8, 3), (11, 1), (20, 2), (18, 1), (100, 2), (15, 2)]
# sum = 187

results = []


def retrieve_value(task, values):
    value, delay = task
    time.sleep(delay)
    values.append(value)
    return value


def sum_tasks(tasks):
    values = []
    threads = []

    for task in tasks:
        thread = Thread(target=retrieve_value, args=(task, values))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    return sum(values)


def run_tasks():
    start = time.perf_counter()
    print('sum', sum_tasks(tasks))

    end = time.perf_counter()

    print(f'ran for {end - start:.2f} seconds')


# Threads can not be terminated
# Threads share memory and resources within the same process
# This can cause thread interference

run_tasks()
