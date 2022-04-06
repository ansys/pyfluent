"""Module providing asynchronous execution functionality."""

from concurrent.futures import ThreadPoolExecutor
import functools


def asynchronous(f):
    """Use for decorating functions to execute asynchronously."""

    @functools.wraps(f)
    def func(*args, **kwargs):
        return ThreadPoolExecutor(max_workers=1).submit(f, *args, **kwargs)

    return func
