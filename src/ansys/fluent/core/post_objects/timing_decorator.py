"""Provides a module for the timing function decorator."""

import time


def timing(func):
    """Decorates timing function."""

    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print(func.__name__, t2 - t1)
        return res

    return wrapper
