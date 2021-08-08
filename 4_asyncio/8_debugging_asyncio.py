"""Debugging Asyncio

Manual Debug
    - print the stack of a task. task.print_stack()

Enabling debug mode:
    - Setting PYTHONASYNCIODEBUG env variable to 1(True)
    - Using the -X dev Python commandline option
    - Passing debug=True to asyncio.run()
    - Calling loop.set_debug

With debug mode enabled:
    - checks for never awaited coroutines and logs them.
    - Non-threadsafe asyncio api raise an exception when called from a wrong thread
    - callbacks taking longer than 100ms are logged. Use loop.slow_callback_duration to
    set the minimum duration on seconds.

Debugging in production
from aiodebug import log_slow_callbacks
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor


# Manual debugging
async def monitor_tasks():
    while True:
        tasks = [
            task for task in asyncio.all_tasks()
            if task is not asyncio.current_task()
        ]

        if not tasks:
            break
        [task.print_stack(limit=5) for task in tasks]
        await asyncio.sleep(1)


class Message(dict):
    def __init__(self, **content):
        super().__init__()
        self.content = content
        for k, v in content.items():
            self[k] = v

    def __repr__(self):
        return f'Message(**{self.content})'


async def handle_message(msg):
    print(msg)


def handle_message_sync(loop, **content):
    msg = Message(**content)
    print(f'Pulled {msg}')
    loop.create_task(handle_message(msg))


def threaded_consumer(loop):
    print('running threaded consumer')
    handle_message_sync(loop, **{'to': 'test', 'from': 'from test', 'message': 'test msg'})


async def main():
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor()
    await loop.run_in_executor(executor, threaded_consumer, loop)


# loop = asyncio.get_event_loop()
# loop.set_debug(True)
# loop.run_until_complete(main())

asyncio.run(main())
