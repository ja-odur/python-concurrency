import asyncio
from concurrent.futures import ThreadPoolExecutor


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
    # loop.create_task(handle_message(msg))
    asyncio.run_coroutine_threadsafe(handle_message(msg), loop)
    # running a coroutine on the main event from another thread
    # i.e working with threads ans asyncio when there are some shared state


def threaded_consumer(loop):
    print('running threaded consumer')
    handle_message_sync(loop, **{'to': 'test', 'from': 'from test', 'message': 'test msg'})


async def main():
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor()
    await loop.run_in_executor(executor, threaded_consumer, loop)


asyncio.run(main(), debug=True)