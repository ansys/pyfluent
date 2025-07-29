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

import pytest

import ansys.fluent.core as pyfluent


@pytest.fixture
def reset_examples_path():
    """Reset both deprecated var and config after each test."""
    yield
    try:
        delattr(pyfluent, "EXAMPLES_PATH")
        delattr(pyfluent.config, "_examples_path")
    except AttributeError:
        pass


def test_default(reset_examples_path):
    # Both deprecated var and config should have the same default value
    with pytest.warns(pyfluent.PyFluentDeprecationWarning):
        assert "ansys_fluent_core_examples" in pyfluent.EXAMPLES_PATH
    assert "ansys_fluent_core_examples" in pyfluent.config.examples_path


def test_get_set_config(reset_examples_path):
    # Set config
    new_path = "/new/path/to/examples"
    pyfluent.config.examples_path = new_path

    # Both deprecated var and config should have the new value
    with pytest.warns(pyfluent.PyFluentDeprecationWarning):
        assert pyfluent.EXAMPLES_PATH == new_path
    assert pyfluent.config.examples_path == new_path


def test_get_set_deprecated_var(reset_examples_path):
    # Set deprecated var
    new_path = "/new/path/to/examples"
    pyfluent.EXAMPLES_PATH = new_path

    # Both deprecated var and config should have the new value
    assert pyfluent.EXAMPLES_PATH == new_path
    assert pyfluent.config.examples_path == new_path


def test_set_config_after_deprecated_var(reset_examples_path):
    # Set deprecated var
    new_path1 = "new_path1"
    pyfluent.EXAMPLES_PATH = new_path1

    # Both deprecated var and config should have the new value
    assert pyfluent.EXAMPLES_PATH == new_path1
    assert pyfluent.config.examples_path == new_path1

    # Set config
    new_path2 = "new_path2"
    with pytest.warns():
        pyfluent.config.examples_path = new_path2

    # Both deprecated var and config should have the latest value
    with pytest.warns(pyfluent.PyFluentDeprecationWarning):
        assert pyfluent.EXAMPLES_PATH == new_path2
    assert pyfluent.config.examples_path == new_path2


def test_set_deprecated_var_after_config(reset_examples_path):
    # Set deprecated var
    new_path1 = "new_path1"
    pyfluent.config.examples_path = new_path1

    # Both deprecated var and config should have the new value
    with pytest.warns(pyfluent.PyFluentDeprecationWarning):
        assert pyfluent.EXAMPLES_PATH == new_path1
    assert pyfluent.config.examples_path == new_path1

    # Set config
    new_path2 = "new_path2"
    pyfluent.EXAMPLES_PATH = new_path2

    # Both deprecated var and config should have the latest value
    assert pyfluent.EXAMPLES_PATH == new_path2
    assert pyfluent.config.examples_path == new_path2
