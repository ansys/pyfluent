"""Module providing asynchronous execution functionality"""

import functools
from concurrent.futures import ThreadPoolExecutor


def asynchronous(f):
    """
    Decorator to execute functions asynchronously
    """

    @functools.wraps(f)
    def func(*args, **kwargs):
        return ThreadPoolExecutor(max_workers=1).submit(f, *args, **kwargs)

    return func
