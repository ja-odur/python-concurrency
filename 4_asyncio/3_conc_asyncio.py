import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

tasks = [say_after(4, 'hello'), say_after(2, 'world'), say_after(6, 'last one')]


async def main():
    task1 = asyncio.create_task(say_after(4, 'hello'))

    task2 = asyncio.create_task(say_after(2, 'world'))

    # This works in all Python versions but is less readable
    task3 = asyncio.ensure_future(say_after(300, 'other'))

    start = time.perf_counter()

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    # Task 3 is cancelled
    task3.cancel()

    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')


# can use gather to start coroutine concurrently, though taska can not be cancelled individually
async def other_method():
    start = time.perf_counter()
    results = await asyncio.wait(tasks)
    print('result', results)
    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')

#
# asyncio.run(main())
#
asyncio.run(other_method())
