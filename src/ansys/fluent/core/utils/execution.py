"""Module providing additional execution methods."""
from concurrent.futures import ThreadPoolExecutor
import functools
from multiprocessing.context import TimeoutError
import multiprocessing.pool
import time
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


def timeout_exec(obj, timeout, args=None, kwargs=None):
    """Executes object with the timeout limit.

    Examples
    --------
    Execute ``time.sleep()`` for 2 seconds, with a timeout of 1 second:

    >>> import time
    >>> from ansys.fluent.core.utils.execution import timeout_exec
    >>> ret = timeout_exec(time.sleep,timeout=1,args=(2,))
    >>> assert ret is False
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    def _exec(*_args, **_kwargs):
        if callable(obj):
            return obj(*_args, **_kwargs)
        else:
            return obj

    pool = multiprocessing.pool.ThreadPool(processes=1)
    async_result = pool.apply_async(_exec, args=args, kwds=kwargs)
    try:
        return_obj = async_result.get(timeout=timeout)
        pool.close()
        if return_obj is None:
            return True
        return return_obj
    except TimeoutError:
        pool.terminate()
        return False


def timeout_loop(
    obj, timeout, args=None, kwargs=None, idle_period=0.2, expected="truthy"
):
    """Loops while specified object does not return expected response. Timeouts after specified time has elapsed."""
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    def _exec(*_args, **_kwargs):
        if callable(obj):
            return obj(*_args, **_kwargs)
        else:
            return obj

    time_elapsed = 0.0
    while time_elapsed <= timeout:
        ret_obj = _exec(*args, **kwargs)
        if expected == "truthy":
            if ret_obj:
                return ret_obj
        elif expected == "falsy":
            if not ret_obj:
                return ret_obj
        else:
            raise RuntimeError(
                "Unrecognized value for 'expected' variable. Accepted: 'truthy' or 'falsy'."
            )
        time.sleep(idle_period)
        time_elapsed += idle_period

    if expected == "truthy":
        return False
    elif expected == "falsy":
        return True
