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

"""Tests for runtime type-checking."""

import os
import subprocess
import sys

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import _type_checking

# The import hook is installed while PyFluent is imported, which has already
# happened by the time these tests run. Anything which depends on the state of
# the hook therefore has to be exercised in a fresh interpreter.


def _run(source: str, enabled: bool) -> str:
    """Run ``source`` in a fresh interpreter and return its stripped output."""
    env = os.environ.copy()
    if enabled:
        env[_type_checking.ENV_VAR] = "1"
    else:
        env.pop(_type_checking.ENV_VAR, None)
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().splitlines()[-1]


@pytest.mark.parametrize("enabled", [False, True])
def test_hook_installed_only_when_env_var_is_set(enabled):
    pytest.importorskip("beartype")
    source = (
        "from ansys.fluent.core import _type_checking\n"
        "print(_type_checking.is_type_checking_enabled())"
    )
    assert _run(source, enabled=enabled) == str(enabled)


@pytest.mark.parametrize("enabled", [False, True])
def test_config_reflects_hook_state(enabled):
    pytest.importorskip("beartype")
    source = (
        "import ansys.fluent.core as pyfluent\n"
        "print(pyfluent.config.runtime_type_checking)"
    )
    assert _run(source, enabled=enabled) == str(enabled)


@pytest.mark.parametrize(
    "enabled, expected",
    [
        # With type-checking on, the bad argument is reported at the call
        # boundary. With it off, it surfaces later as an obscure downstream
        # error.
        (True, "BeartypeCallHintParamViolation"),
        (False, "AttributeError"),
    ],
)
def test_type_violation_is_reported_only_when_enabled(enabled, expected):
    pytest.importorskip("beartype")
    source = (
        "from ansys.fluent.core.utils.fluent_version import get_version_for_file_name\n"
        "try:\n"
        "    get_version_for_file_name(version=123)\n"
        "    print('no-raise')\n"
        "except Exception as exc:\n"
        "    print(type(exc).__name__)"
    )
    assert _run(source, enabled=enabled) == expected


def test_import_succeeds_with_type_checking_enabled():
    pytest.importorskip("beartype")
    source = "import ansys.fluent.core\nprint('imported')"
    assert _run(source, enabled=True) == "imported"


def test_runtime_type_check_is_a_no_op_when_disabled():
    def fn(x: int) -> int:
        return x

    assert _type_checking.runtime_type_check(fn) is fn


def test_runtime_type_check_uses_the_active_backend(monkeypatch):
    pytest.importorskip("beartype")
    from beartype.roar import BeartypeCallHintParamViolation

    monkeypatch.setattr(_type_checking, "_HOOK_INSTALLED", True)

    @_type_checking.runtime_type_check
    def fn(x: int) -> int:
        return x

    assert fn(1) == 1
    with pytest.raises(BeartypeCallHintParamViolation):
        fn("1")


def test_backend_is_swappable(monkeypatch):
    monkeypatch.setattr(_type_checking, "_HOOK_INSTALLED", True)
    monkeypatch.setattr(_type_checking, "BACKEND", "none")

    def fn(x: int) -> int:
        return x

    assert _type_checking.runtime_type_check(fn) is fn
    assert _type_checking._BACKENDS["none"]["install_hook"]() is False


def test_no_runtime_type_check_marks_the_object():
    def fn(x: int) -> int:
        return x

    assert _type_checking.no_runtime_type_check(fn).__no_type_check__ is True


def test_install_import_hook_is_a_no_op_without_the_env_var(monkeypatch):
    monkeypatch.delenv(_type_checking.ENV_VAR, raising=False)
    monkeypatch.setattr(_type_checking, "_HOOK_INSTALLED", False)
    assert _type_checking.install_import_hook() is False
    assert _type_checking.is_type_checking_enabled() is False


def test_install_import_hook_is_idempotent(monkeypatch):
    monkeypatch.setenv(_type_checking.ENV_VAR, "1")
    monkeypatch.setattr(_type_checking, "_HOOK_INSTALLED", True)
    assert _type_checking.install_import_hook() is False


def test_install_import_hook_warns_when_the_backend_is_missing(monkeypatch):
    def _raise():
        raise ImportError("No module named 'beartype'")

    monkeypatch.setenv(_type_checking.ENV_VAR, "1")
    monkeypatch.setattr(_type_checking, "_HOOK_INSTALLED", False)
    monkeypatch.setitem(
        _type_checking._BACKENDS[_type_checking.BACKEND], "install_hook", _raise
    )
    with pytest.warns(UserWarning, match="runtime type-checking is disabled"):
        assert _type_checking.install_import_hook() is False
    assert _type_checking.is_type_checking_enabled() is False


def test_config_warns_when_set_after_import(monkeypatch):
    monkeypatch.delattr(pyfluent.config, "_runtime_type_checking", raising=False)
    with pytest.warns(
        UserWarning, match="cannot be changed after PyFluent is imported"
    ):
        pyfluent.config.runtime_type_checking = (
            not _type_checking.is_type_checking_enabled()
        )
    monkeypatch.delattr(pyfluent.config, "_runtime_type_checking", raising=False)


def test_config_print_includes_runtime_type_checking(capsys):
    pyfluent.config.print()
    assert "runtime_type_checking" in capsys.readouterr().out
