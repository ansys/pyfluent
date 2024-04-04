"""Provides a module for timing function decorator."""

import time


def timing(func):
    """Timing function decorator."""

    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print(func.__name__, t2 - t1)
        return res

    return wrapper
