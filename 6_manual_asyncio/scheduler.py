import time
from collections import deque
import heapq


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = []
        self.sequence = 0

    def call_soon(self, func):
        self.ready.append(func)

    def call_later(self, delay, func):
        self.sequence += 1
        deadline = time.time() + delay
        heapq.heappush(self.sleeping, (deadline, self.sequence, func))

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, func = heapq.heappop(self.sleeping)
                delta = deadline - time.time()

                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)

            while self.ready:
                func = self.ready.popleft()
                func()


sched = Scheduler()


def countdown(start):
    if start > 0:
        print('Down', start)
        sched.call_later(4, lambda: countdown(start-1))


def count_up(stop):
    def _run(start):
        if start < stop:
            print('UP', start)
            sched.call_later(1, lambda: _run(start+1))
    _run(0)



def cd(start):
    while start > 0:
        print('Down', start)
        time.sleep(1)
        start -= 1


def cu(end):
    start = 0
    while start < end:
        print('Up', start)
        time.sleep(1)
        start += 1

# cd(5)
# cu(5)


if __name__ == '__main__':
    sched.call_soon(lambda: countdown(5))
    sched.call_soon(lambda: count_up(20))
    sched.run()