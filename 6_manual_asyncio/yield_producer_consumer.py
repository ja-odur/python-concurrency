from collections import deque
from yield_scheduler import switch, Scheduler


sched = Scheduler()


class QueueClosed(Exception):
    pass


class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()
        self._closed = False

    def close(self):
        self._closed = True
        if self.waiting and not self.items:
            sched.ready.append(self.waiting.popleft())

    async def put(self, item):
        if self._closed:
            raise QueueClosed()

        self.items.append(item)
        if self.waiting:
            sched.ready.append(self.waiting.popleft())

    async def get(self):
        while not self.items:
            if self._closed:
                raise QueueClosed()
            self.waiting.append(sched.current)
            sched.current = None
            await switch()
        return self.items.popleft()


async def producer(q, count):
    for n in range(count):
        print('Producing', n)
        await q.put(n)
        await sched.sleep(1)

    print('Produce done')
    q.close()


async def consumer(q):
    try:
        while True:
            item = await q.get()
            if item is None:
                break
            print('Consuming', item)
    except QueueClosed:
        print('Consumer done')


if __name__ == "__main__":
    q = AsyncQueue()
    sched.new_task(producer(q, 10))
    sched.new_task(consumer(q))
    sched.run()