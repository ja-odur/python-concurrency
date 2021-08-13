import time
from collections import deque
import heapq


class Awaitable:
    def __await__(self):
        yield


def switch():
    return Awaitable()


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = []
        self.sequence = 0
        self.current = None

    async def sleep(self, delay):
        self.sequence += 1
        deadline = time.time() + delay
        heapq.heappush(self.sleeping, (deadline, self.sequence, self.current))
        self.current = None
        await switch()

    def new_task(self, gen):
        self.ready.append(gen)

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, coro = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(coro)

            self.current = self.ready.popleft()
            # Drive it as a generator
            try:
                self.current.send(None)
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass


sched = Scheduler()


async def countdown(n):
    while n > 0:
        print('Down', n)
        await sched.sleep(4)
        n -= 1


async def count_up(stop):
    x = 0
    while x < stop:
        print('Up', x)
        await sched.sleep(1)
        x += 1


if __name__ == '__main__':
    sched.new_task(countdown(5))
    sched.new_task(count_up(20))
    sched.run()
