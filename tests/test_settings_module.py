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

import pytest

from ansys.fluent.core.diagnostics.exceptions import PyFluentUserWarning
from ansys.fluent.core.solver import settings, using


def test_settings_module_no_session_exposes_static_metadata():
    with pytest.warns(PyFluentUserWarning):
        setup = settings.setup
    assert "boundary_conditions" in setup.child_names
    assert "boundary_conditions" in setup._child_classes


def test_settings_module_no_session_live_call_raises_clear_error():
    with pytest.warns(PyFluentUserWarning):
        setup = settings.setup
    with pytest.raises(RuntimeError, match="requires a live Fluent session"):
        setup.get_active_child_names()


def test_settings_module_dir_lists_known_names():
    names = dir(settings)
    assert "setup" in names
    assert "solution" in names


def test_settings_module_unknown_attribute_raises():
    with pytest.warns(PyFluentUserWarning):
        with pytest.raises(AttributeError):
            settings.this_attribute_does_not_exist


@pytest.mark.fluent_version(">=24.2")
def test_settings_module_binds_to_active_session(mixing_elbow_case_data_session):
    solver = mixing_elbow_case_data_session
    with using(solver):
        assert settings.setup == solver.settings.setup
        assert settings.solution == solver.settings.solution


@pytest.mark.fluent_version(">=24.2")
def test_inactive_and_active_sessions(mixing_elbow_case_data_session):
    # Test that accessing settings without an active session raises a warning
    with pytest.warns(PyFluentUserWarning):
        setup = settings.setup
    assert {
        "child_names",
        "command_names",
        "get_active_child_names",
        "get_active_command_names",
    }.issubset(set(dir(settings.setup)))
    assert {"general", "models", "boundary_conditions"}.issubset(
        set(settings.setup.child_names)
    )
    with pytest.raises(RuntimeError, match="requires a live Fluent session"):
        setup.get_active_child_names()
    assert "velocity_inlet" in settings.boundary_conditions.child_names
    solver = mixing_elbow_case_data_session
    with using(solver):
        assert settings.setup == solver.settings.setup
        assert {"general", "models", "boundary_conditions"}.issubset(
            set(settings.setup.get_active_child_names())
        )
        assert settings.solution == solver.settings.solution
