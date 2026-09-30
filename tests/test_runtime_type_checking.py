# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Tests for the ``no_runtime_type_check`` marker.

PyFluent does not install or activate any runtime type-checker itself; a user
who wants one applies it themselves (e.g. via ``beartype.claw``) over their own
environment. These tests only cover the marker that lets such a checker skip
PyFluent's dynamic proxy/generic classes, plus a smoke test simulating that
user-applied workflow.
"""

import subprocess
import sys

import pytest

from ansys.fluent.core import _type_checking


def test_no_runtime_type_check_marks_a_function():
    def fn(x: int) -> int:
        return x

    assert _type_checking.no_runtime_type_check(fn).__no_type_check__ is True


def test_no_runtime_type_check_marks_a_class():
    @_type_checking.no_runtime_type_check
    class Foo:
        pass

    assert Foo.__no_type_check__ is True


def test_no_runtime_type_check_skips_generic_alias():
    # e.g. SettingsBase[DictStateType], which does not support attribute assignment.
    alias = list[int]
    assert _type_checking.no_runtime_type_check(alias) is alias


def _run(source: str) -> str:
    """Run ``source`` in a fresh interpreter and return its stripped output."""
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().splitlines()[-1]


def test_user_applied_checker_does_not_crash_on_a_checked_submodule():
    """Simulates a user applying beartype to a specific submodule themselves.

    The hook targets a single submodule here rather than the whole
    ``ansys.fluent.core`` package: some other modules still contain
    ``TYPE_CHECKING``-only forward references that a runtime checker cannot
    resolve eagerly, which is a pre-existing, tracked limitation independent
    of this marker mechanism.
    """
    pytest.importorskip("beartype")
    source = (
        "from beartype.claw import beartype_package\n"
        "beartype_package('ansys.fluent.core.utils.fluent_version')\n"
        "import ansys.fluent.core.utils.fluent_version\n"
        "print('imported')"
    )
    assert _run(source) == "imported"


def test_user_applied_checker_reports_violations():
    """A genuine violation still raises the user's own checker's exception."""
    pytest.importorskip("beartype")
    source = (
        "from beartype.claw import beartype_package\n"
        "beartype_package('ansys.fluent.core.utils.fluent_version')\n"
        "from ansys.fluent.core.utils.fluent_version import get_version_for_file_name\n"
        "try:\n"
        "    get_version_for_file_name(version=123)\n"
        "    print('no-raise')\n"
        "except Exception as exc:\n"
        "    print(type(exc).__name__)"
    )
    assert _run(source) == "BeartypeCallHintParamViolation"
