import asyncio
import concurrent.futures
import time


def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    time.sleep(2)
    return 'done blocking io'


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    time.sleep(2)
    s = sum(i * i for i in range(10 ** 7))
    return s



async def main():
    loop = asyncio.get_running_loop()

    ## Options:
    start = time.perf_counter()
    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print('custom thread pool', result)

    # 3. Run in a custom process pool:
    # Needs to be guarded using __name__ == '__main__' to avoid error
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print('custom process pool', result)

    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')


async def thread(loop, job):
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, job)


async def process(loop, job):
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, job)

async def monitor_tasks():
    while True:
        tasks = [
            task for task in asyncio.all_tasks()
            if task is not asyncio.current_task()
        ]

        if not tasks:
            continue
        [task.print_stack(limit=5) for task in tasks]
        await asyncio.sleep(1)

async def main_conc():
    loop = asyncio.get_running_loop()
    tasks = [thread(loop, blocking_io), thread(loop, blocking_io), process(loop, cpu_bound)]
    start = time.perf_counter()
    # asyncio.create_task(monitor_tasks())

    results = await asyncio.wait(tasks)
    print(f'combined results -> {[[task .result() for task in task_set] for task_set in results]}')
    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')


async def run_process(loop):
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print('custom process pool', result)

    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')

# asyncio.run(main())
if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(run_process(loop))

    asyncio.run(main_conc())
