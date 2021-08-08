# from threading import Lock
#
#
# def lock_class(methodnames, lockfactory):
#     print('creating wrapper')
#     return lambda cls: make_threadsafe(cls, methodnames, lockfactory)
#
#
# def lock_(methodnames, lockfactory):
#     def decorator(cls):
#         return make_threadsafe(cls, methodnames, lockfactory)
#
#     return decorator
#
#
# def lock_method(method):
#     if getattr(method, '__is_locked', False):
#         raise TypeError("Method %r is already locked!" % method)
#
#     def locked_method(self, *arg, **kwarg):
#         print('this is a locked method')
#         with self._lock:
#             return method(self, *arg, **kwarg)
#     locked_method.__name__ = '%s(%s)' % ('lock_method', method.__name__)
#     locked_method.__is_locked = True
#     return locked_method
#
#
# def make_threadsafe(cls, methodnames, lockfactory):
#     init = cls.__init__
#     def newinit(self, *arg, **kwarg):
#         init(self, *arg, **kwarg)
#         self._lock = lockfactory()
#     cls.__init__ = newinit
#
#     for methodname in methodnames:
#         oldmethod = getattr(cls, methodname)
#         newmethod = lock_method(oldmethod)
#         setattr(cls, methodname, newmethod)
#
#     return cls
#
#
# @lock_class(['add','remove'], Lock)
# class ClassDecoratorLockedSet(set):
#
#     @lock_method # if you double-lock a method, a TypeError is raised
#     def lockedMethod(self):
#         print("This section of our code would be thread safe")
#         pass
#
#
# class A(set):
#     pass
#
#
# if __name__ == '__main__':
#     s = ClassDecoratorLockedSet()
#     a = set()
#     a.add(5)
#     print(a)
#     s.add(5)
#     print(s)
#     print(A())

import asyncio
import time

JOB_COUNT = 200
JOB_DURATION = 0.01  # 10ms
WORKER_COUNT = 4

async def heartbeat():
    while True:
        start = time.time()
        await asyncio.sleep(1)
        delay = time.time() - start - 1
        print(f'heartbeat delay = {delay:.3f}s')


async def process():
    time.sleep(JOB_DURATION)

async def main_with_queue():
    asyncio.create_task(heartbeat())

    print('before sleep')
    await asyncio.sleep(2.5)
    print('after sleep')

    queue = asyncio.Queue(maxsize=1)

    async def worker():
        while True:
            print('worker created')
            coro = await queue.get()
            print('job done')
            await coro  # consider using try/except
            queue.task_done()


    workers = [asyncio.create_task(worker())
                   for _ in range(4)]
    print('workers created')

    print('begin processing')
    for _ in range(JOB_COUNT):
        await queue.put(process())
    await queue.join()
    print('end processing')

    for w in workers:
        w.cancel()

    await asyncio.sleep(2)

asyncio.run(main_with_queue())

# before sleep
# heartbeat delay = 0.004s
# heartbeat delay = 0.004s
# after sleep
# begin processing
# heartbeat delay = 0.019s
# heartbeat delay = 0.015s
# end processing
# heartbeat delay = 0.005s
# heartbeat delay = 0.003s
