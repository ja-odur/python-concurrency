import time
tasks = [(5, 4), (10, 1), (8, 3), (11, 1), (20, 2), (18, 1), (100, 2), (15, 2)]
# sum = 14 seconds


def retrieve_value(task):
    value, delay = task
    time.sleep(delay)
    return value


def sum_tasks(tasks):
    sum = 0

    for task in tasks:
        sum += retrieve_value(task)

    return sum


def run_tasks():
    start = time.perf_counter()

    print('sum', sum_tasks(tasks))

    end = time.perf_counter()

    print(f'ran for {end - start:.2f} seconds')


if __name__ == '__main__':
    run_tasks()
