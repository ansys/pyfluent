import time

from ansys.fluent.core.utils.execution import timeout_exec, timeout_loop


def test_timeout_exec():
    ret = timeout_exec(time.sleep, timeout=0.25, args=(0.5,))
    assert ret is False
    ret = timeout_exec(time.sleep, timeout=0.5, args=(0.25,))
    assert ret is True


def test_timeout_loop():
    class ExpectedAfterFive:
        def __init__(self, expected):
            self._counter = 0
            self._expected = expected

        def __call__(self):
            self._counter += 1
            if self._counter >= 5:
                return self._expected
            else:
                return not self._expected

    class Waiter:
        def __init__(self, func, expected):
            self._func = func(expected)
            self._expected = expected

        def __call__(self):
            returned = self._func()
            if returned == self._expected:
                return returned
            else:
                return returned

    waiter = Waiter(ExpectedAfterFive, expected=True)
    ret = timeout_loop(waiter, timeout=1, expected="truthy", idle_period=0.1)
    assert ret is True

    waiter = Waiter(ExpectedAfterFive, expected=False)
    ret = timeout_loop(waiter, timeout=1, expected="falsy", idle_period=0.1)
    assert ret is False

    waiter = Waiter(ExpectedAfterFive, expected=True)
    ret = timeout_loop(waiter, timeout=0.2, expected="truthy", idle_period=0.1)
    assert ret is False


def count_key_recursive(dictionary, key):
    count = 0
    for k, v in dictionary.items():
        if k == key:
            count += 1
        elif isinstance(v, dict):
            count += count_key_recursive(v, key)
    return count
