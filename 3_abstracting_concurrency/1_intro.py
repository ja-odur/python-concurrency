"""
Common operations in Thread or Processing API
thread_or_process = Thread(...) or Process(...)

thread_or_process.start()
thread_or_process.join()
The above operations can be in loops in order to create a pool of workers

In Summary,
1) Create a task
2) Pass task to Executor
3) Get Results

using a high level interface:
1) no need to worry about starting and joining threads or processes
2) we can easily switch between threads and procesess by simply changing the executor

The Executor API provides only three methods
1) submit(fn, *args, **kwargs) for scheduling a function to run. returns future object
2) map(fn, *iterables, timeout=None, chucksize=1)
3) shutdown(wait=True) stop accepting tasks and shutdown once current tasks are done. after shutdown,
any attempt to call submit or map throws an error

concrete executor classes

1) ThreadPoolExecutor(max_workers=None, thread_name_prefix='')
default max_workers = num of cores * 5

2) ProcessPoolExecutor(max_workers=None) which defaults to number of processor cores on the machine

"""
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
import time


urls = ['http://www.cnn.com', 'http://www.unknown-random-site-124556.com']



def load_url(url, timeout):
    with urlopen(url, timeout=timeout) as url_req:
        return url_req.read()

def no_c():
    start = time.perf_counter()
    load_url(urls[0], 60)
    load_url(urls[0], 60)
    end = time.perf_counter()

    print(f'ran for {end - start:.2f} seconds')


with ThreadPoolExecutor(max_workers=2) as executor:
    start = time.perf_counter()
    f1 = executor.submit(load_url, urls[0], 60)
    f2 = executor.submit(load_url, urls[1], 60)

    try:
        data1 = f1.result()
        print(f'{urls[0]} page is {len(data1)} bytes')

        data2 = f2.result()
        print(f'{urls[1]} page is {len(data2)} bytes')

    except Exception as exc:
        print('Error downloading page', exc)

    end = time.perf_counter()
    print(f'ran for {end - start:.2f} seconds')


no_c()
