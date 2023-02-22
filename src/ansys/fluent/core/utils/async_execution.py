"""Module providing asynchronous execution functionality."""

from concurrent.futures import ThreadPoolExecutor
import functools
from typing import Callable


def asynchronous(f: Callable) -> Callable:
    """Use for decorating functions that are to execute asynchronously. The
    decorated function returns a `future`_ object. Calling `result()`_ on the
    future object synchronizes the function execution.

    Examples
    --------
    >>> # asynchronous execution using @asynchronous decorator
    >>> @asynchronous
    ... def asynchronous_solve(session, number_of_iterations):
    ...     session.solver.tui.solve.iterate(number_of_iterations)
    >>> asynchronous_solve(session1, 100)

    >>> # using the asynchronous function directly
    >>> asynchronous(session2.solver.tui.solve.iterate)(100)

    >>> # synchronous execution of above 2 calls
    >>> asynchronous_solve(session1, 100).result()
    >>> asynchronous(session2.solver.tui.solve.iterate)(100).result()

    .. _Future: https://docs.python.org/3/library/asyncio-future.html#future-object  # noqa: E501
    .. _result(): https://docs.python.org/3/library/asyncio-future.html#asyncio.Future.result  # noqa: E501
    """

    @functools.wraps(f)
    def func(*args, **kwargs) -> Callable:
        return ThreadPoolExecutor(max_workers=1).submit(f, *args, **kwargs)

    return func
