"""Profiling asyncio

cProfile:
    - python3.8 -m cProfile -s tottime 8_debugging_asyncio.py

kcachedgrind:
    - python3.8 -m cProfile -o debug.prof  8_debugging_asyncio.py
    - pyprof2calltree --kcachegrind -i 8_debugging_asyncio.py

    dependencies:
        kcachedgrind/qcachedgrind
        pyprof2calltree
"""