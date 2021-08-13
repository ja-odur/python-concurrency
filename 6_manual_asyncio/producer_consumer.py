from collections import deque
from scheduler import Scheduler

sched = Scheduler()


class Result:
    def __init__(self, value=None, exc=None):
        self._exc = exc
        self.result = value

    @property
    def result(self):
        if self._exc:
            raise self._exc
        return self._result

    @result.setter
    def result(self, value):
        self._result = value


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
            for func in self.waiting:
                sched.call_soon(func)

    def put(self, item):
        if self._closed:
            raise QueueClosed()

        self.items.append(item)
        if self.waiting:
            func = self.waiting.popleft()

            sched.call_soon(func)

    def get(self, callback):
        # Wait until an item is available and return it
        if self.items:
            callback(Result(value=self.items.popleft()))
        else:
            if self._closed:
                callback(Result(exc=QueueClosed()))
            self.waiting.append(lambda: self.get(callback))


def producer(q, count):
    def _run(n):
        if n < count:
            print('Producing', n)
            q.put(n)
            sched.call_later(1, lambda: _run(n+1))
        else:
            print('Producer done')
            q.close()
    _run(0)


def consumer(q):
    def _consume(result):
        try:
            item = result.result
            print('Consuming', item)
            sched.call_soon(lambda: consumer(q))
        except QueueClosed:
            print('Consumer done')

    q.get(callback=_consume)


q = AsyncQueue()
sched.call_soon(lambda: producer(q, 10))
sched.call_soon(lambda: consumer(q))
sched.run()
