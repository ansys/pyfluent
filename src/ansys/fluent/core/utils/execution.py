"""Module providing additional execution methods."""

from concurrent.futures import ThreadPoolExecutor
import functools
from multiprocessing.context import TimeoutError
import multiprocessing.pool
import time
from typing import Any, Callable

from ansys.fluent.core.exceptions import InvalidArgument


def asynchronous(f: Callable) -> Callable:
    """Use for decorating functions that are to execute asynchronously. The decorated
    function returns a `future`_ object. Calling `result()`_ on the future object
    synchronizes the function execution.

    Examples
    --------
    asynchronous execution using @asynchronous decorator

    >>> @asynchronous
    ... def asynchronous_solve(solver_session, number_of_iterations):
    ...     solver_session.tui.solve.iterate(number_of_iterations)
    >>> asynchronous_solve(solver_session_1, 100)

    using the asynchronous function directly

    >>> asynchronous(solver_session_2.tui.solve.iterate)(100)

    synchronous execution of above 2 calls

    >>> asynchronous_solve(solver_session_1, 100).result()
    >>> asynchronous(solver_session_2.tui.solve.iterate)(100).result()

    .. _Future: https://docs.python.org/3/library/asyncio-future.html#future-object
    .. _result(): https://docs.python.org/3/library/asyncio-future.html#asyncio.Future.result
    """

    @functools.wraps(f)
    def func(*args, **kwargs) -> Callable:
        return ThreadPoolExecutor(max_workers=1).submit(f, *args, **kwargs)

    return func


def timeout_exec(obj, timeout, args=None, kwargs=None):
    """Executes object with the timeout limit. Tries to return whatever the provided
    object returns. If the object returns nothing, this function will return ``True``.
    If it times out, returns ``False``.

    Parameters
    ----------
    obj : Any
        Object to execute.
    timeout : float
        Time before cancelling execution and returning early.
    args : Any, optional
        Arguments to be passed to the specified object.
    kwargs : Any, optional
        Keyword arguments to be passed to the specified object.

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
        if not return_obj and return_obj is not False:
            return True
        return return_obj
    except TimeoutError:
        pool.terminate()
        return False


def timeout_loop(
    obj: Any,
    timeout: float,
    args: Any | None = None,
    kwargs: Any | None = None,
    idle_period: float = 0.2,
    expected: str = "truthy",
) -> Any:
    """Loops while specified object does not return expected response. Timeouts after
    specified time has elapsed. Tries to return whatever is returned by the specified
    object. If nothing is returned before timeout, returns the opposite of the expected
    value, i.e. ``True`` if ``expected == "falsy"`` and ``False`` if ``expected ==
    "truthy"``.

    Parameters
    ----------
    obj : Any
        Object to evaluate while looping if it does not return expected response.
    timeout : float
        Time before cancelling execution and returning early.
    args : Any, optional
        Arguments to be passed to the specified object.
    kwargs : Any, optional
        Keyword arguments to be passed to the specified object.
    idle_period : float, optional
        Time in seconds to wait between object evaluations, defaults to 0.2 seconds.
    expected: str, optional
        Possible values are ``"truthy"`` or ``"falsy"``, indicating what type of return is expected.
        By default, expects a ``"truthy"`` return from the specified object.

    Raises
    ------
    InvalidArgument
        If an unrecognized value is passed for ``expected``.

    Examples
    --------
    Waiting 5 seconds to see if ``func("test")`` returns True:

    >>> func("test")
    False
    >>> response = timeout_loop(func, timeout=5.0, args=("test",))

    Waiting 5 seconds to see if ``func2("test",word="hello")`` returns False:

    >>> func2("test", word="hello")
    True
    >>> response = timeout_loop(func2, timeout=5.0, expected="falsy", args=("test",), kwargs={"word":"hello",})
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
            raise InvalidArgument("Specify 'expected' as either 'truthy' or 'falsy'.")
        time.sleep(idle_period)
        time_elapsed += idle_period

    if expected == "truthy":
        return False
    elif expected == "falsy":
        return True
