import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    start = time.perf_counter()

    await say_after(2, 'hello')
    await say_after(1, 'world')

    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')

asyncio.run(main())
