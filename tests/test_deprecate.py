# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

import warnings

import pytest

from ansys.fluent.core import PyFluentDeprecationWarning
from ansys.fluent.core.utils.deprecate import deprecate_arguments, deprecate_function


def test_deprecate_argument_warns():
    """Test that deprecated arguments triggers a warning and maps correctly."""

    @deprecate_arguments(old_args=["a", "b"], new_args=["d", "e"], version="3.0.0")
    @deprecate_arguments(old_args="c", new_args="f", version="3.0.0")
    @deprecate_arguments(old_args="x1", new_args="z1", version="3.0.0")
    def example_func(**kwargs):
        assert "d" in kwargs
        assert "f" in kwargs
        assert "z1" in kwargs
        assert "a" not in kwargs
        assert "c" not in kwargs
        assert "x1" not in kwargs
        return kwargs

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # ensure deprecation warnings are captured
        result = example_func(a=1, b=2, c=3, x1=2, x2=4)

    # Check that the warnings were raised
    assert len(w) == 6
    warning = w[0]
    assert issubclass(warning.category, PyFluentDeprecationWarning)
    assert "'a', 'b'" in str(warning.message)
    assert "'d', 'e'" in str(warning.message)

    # Check that function received the new argument
    assert result == {"d": 1, "e": 2, "f": 3, "x2": 4, "z1": 2}


def test_deprecate_argument_warns_with_custom_converter():
    """Test that deprecated arguments triggers a warning and maps correctly."""

    def my_custom_converter(kwargs, old_args, new_args):
        # Combine values of a, b into a tuple → d
        values = tuple(kwargs.pop(arg) for arg in old_args if arg in kwargs)
        if values:
            kwargs[new_args[0]] = values
        return kwargs

    @deprecate_arguments(
        old_args=["a", "b"],
        new_args="d",
        version="3.0.0",
        converter=my_custom_converter,
    )
    @deprecate_arguments(
        old_args="c",
        new_args="e",
        version="3.0.0",
    )
    def example_func(**kwargs):
        assert "d" in kwargs
        assert "e" in kwargs
        assert "c" not in kwargs
        assert "a" not in kwargs
        return kwargs

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # ensure deprecation warnings are captured
        result = example_func(a=1, b=2, c=3)

    # Check that the warnings were raised
    assert len(w) == 4
    warning = w[0]
    assert issubclass(warning.category, PyFluentDeprecationWarning)
    assert "'a', 'b'" in str(warning.message)
    assert "'d'" in str(warning.message)

    assert result == {"d": (1, 2), "e": 3}


def test_deprecate_argument_raises_value_error_without_converter():
    """Test that deprecated arguments raises ValueError for incorrect mapping."""

    with pytest.raises(ValueError):

        @deprecate_arguments(
            old_args=["a", "b"],
            new_args="d",
            version="3.0.0",
        )
        def example_func_1(**kwargs):
            assert "d" in kwargs
            assert "e" in kwargs
            assert "c" not in kwargs
            assert "a" not in kwargs
            return kwargs

    with pytest.raises(ValueError):

        @deprecate_arguments(
            old_args="a",
            new_args=["d", "e"],
            version="3.0.0",
        )
        def example_func_2(**kwargs):
            assert "d" in kwargs
            assert "e" in kwargs
            assert "c" not in kwargs
            assert "a" not in kwargs
            return kwargs


def test_deprecate_function():
    """Test that deprecated function display warning."""

    @deprecate_function(version="3.0.0", new_func="new_add")
    def old_add(a, b):
        return a + b

    def new_add(a, b):
        return a + b + 10

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # ensure deprecation warnings are captured
        result = old_add(1, 2)

    # Check that the warnings were raised
    assert len(w) == 2
    warning = w[0]
    assert issubclass(warning.category, PyFluentDeprecationWarning)
    assert "'old_add'" in str(warning.message)
    assert "'new_add'" in str(warning.message)
    assert "3.0.0" in str(warning.message)

    assert result == 3
