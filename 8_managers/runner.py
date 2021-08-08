import asyncio
from manager import Manager


async def test_one(end):
    counter = 0
    while counter < end:
        print(f'test 1 counter {counter}')
        counter += 1
        await asyncio.sleep(1)


async def test_2(end):
    counter = 0
    while counter < end:
        print(f'test 2 counter {counter}')
        counter += 1
        await asyncio.sleep(2)


def test_3():
    print('blocking call 3')


async def main():
    print('starting manager')
    manager = Manager()
    manager.register('test-1', test_one)
    manager.register('test-2', test_2)
    manager.register('test-3', test_3)

    await manager.wait(manager.emit('test-2', 3))
    # await test_one(5)
    # manager.emit('test-3')
    print('end')
    await asyncio.sleep(100)
    print('ending manager')


if __name__ == '__main__':
    asyncio.run(main())
