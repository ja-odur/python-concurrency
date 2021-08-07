import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    start = time.perf_counter()

    await say_after(1, 'hello')
    await say_after(2, 'world')

    end = time.perf_counter()

    print(f'Ran in {end - start:.2f} seconds')

# does not work
# Because executing a coroutine function doesnot result into the execution of the function block but rather
# returns a coroutine object
main()
# type(main())


#To actually run a coroutine, asyncio provides three main mechanisms:
# 1)The asyncio.run() function to run the top-level entry point “main()” function (see the above example.)
print('using asyncio.run')
asyncio.run(main())

# 2) Awaiting on a coroutine. The following snippet of code will print “hello” after waiting for 1 second,
# and then print “world” after waiting for another 2 seconds:


print('using await')
async def wrapper():
    await main()

loop = asyncio.new_event_loop()
loop.run_until_complete(wrapper())
loop.close()