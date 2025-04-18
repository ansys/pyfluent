# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

import pytest

from ansys.fluent.core.utils.dictionary_operations import get_first_dict_key_for_value
from ansys.fluent.core.utils.execution import (
    InvalidArgument,
    timeout_exec,
    timeout_loop,
)


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

    with pytest.raises(InvalidArgument):
        timeout_loop(waiter, timeout=0.2, expected=True, idle_period=0.1)


def count_key_recursive(dictionary, key):
    count = 0
    for k, v in dictionary.items():
        if k == key:
            count += 1
        elif isinstance(v, dict):
            count += count_key_recursive(v, key)
    return count


def test_get_first_dict_key_for_value():
    assert get_first_dict_key_for_value({1: 2}, 2) == 1
    assert get_first_dict_key_for_value({1: 2, 3: 4}, 2) == 1
    with pytest.raises(ValueError):
        get_first_dict_key_for_value({1: 2}, 1)


PYTEST_RELATIVE_TOLERANCE = 1e-3


def pytest_approx(expected):
    return pytest.approx(expected=expected, rel=PYTEST_RELATIVE_TOLERANCE)
