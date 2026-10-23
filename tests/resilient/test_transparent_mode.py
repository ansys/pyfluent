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

"""Tests for transparent resilient mode.

These assert that after ``enable_resilient_mode`` the ordinary settings-service
calls (``set_var`` / ``execute_cmd``) -- the ones every ``obj.x = v`` and
``command(...)`` on the settings tree funnels through -- are transparently
classified, auto-recovered, auto-checkpointed and (with a pool) failed over,
without any change to the user API.
"""

import pytest

from ansys.fluent.core.resilient.attach import (
    enable_resilient_mode,
    is_resilient,
    last_outcome,
)
from ansys.fluent.core.resilient.exceptions import UnrecoverableStepError
from ansys.fluent.core.resilient.filecheck import FileCheckpointConfig
from ansys.fluent.core.resilient.interceptor import ResilientSettingsService
from ansys.fluent.core.resilient.solver import ResilientConfig
from ansys.fluent.core.resilient.types import CheckpointKind
from tests.resilient._fakes import (
    FakeFileGroup,
    FakeGroup,
    FakeLeaf,
    FakeSession,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


def _config(tmp_path, **kw):
    return ResilientConfig(
        file_checkpoint=FileCheckpointConfig(directory=str(tmp_path)), **kw
    )


def _elbow_session():
    def reject_high_ti(value):
        if isinstance(value, (int, float)) and value > 1.0:
            raise RuntimeError("Value is not in range\nError Object: (0 1)")

    settings = FakeSettings(
        file_group=FakeFileGroup(),
        setup=FakeGroup(
            models=FakeGroup(energy=FakeGroup(enabled=FakeLeaf(False))),
            turbulence=FakeGroup(
                intensity=FakeLeaf(
                    0.05, minimum=0.0, maximum=1.0, set_raises=reject_high_ti
                )
            ),
        ),
    )
    return FakeSession(settings=settings)


def test_enable_wraps_service_and_is_detectable(tmp_path):
    session = _elbow_session()
    enable_resilient_mode(session, _config(tmp_path))
    assert is_resilient(session)
    assert isinstance(session._settings_service, ResilientSettingsService)
    # The convenience methods are attached.
    assert callable(session.checkpoint)
    assert callable(session.undo)
    assert callable(session.redo)
    assert callable(session.rewind_to)


def test_normal_set_goes_through_interceptor(tmp_path):
    session = _elbow_session()
    enable_resilient_mode(session, _config(tmp_path))
    # Ordinary settings-service write (what obj.x = v funnels through).
    session._settings_service.set_var("setup.models.energy.enabled", True)
    assert session.settings.setup.models.energy.enabled.get_state() is True
    assert last_outcome(session).ok


def test_out_of_range_auto_recovered_transparently(tmp_path):
    session = _elbow_session()
    enable_resilient_mode(session, _config(tmp_path))
    # A bad value is rejected by Fluent, then clamped + retried automatically.
    session._settings_service.set_var("setup.turbulence.intensity", 5.0)
    out = last_outcome(session)
    assert out.ok and "clamp" in out.fixes_applied
    assert session.settings.setup.turbulence.intensity.get_state() == 1.0


def test_irreversible_command_auto_checkpoints(tmp_path):
    session = _elbow_session()
    # Give the session an iterate command under solution.run_calculation.
    session.settings.solution = FakeGroup(run_calculation=FakeGroup(iterate=_Iterate()))
    enable_resilient_mode(session, _config(tmp_path))
    session._settings_service.execute_cmd(
        "solution.run_calculation", "iterate", iter_count=10
    )
    # A file checkpoint was written before the irreversible command.
    assert any(c[0] == "write_case_data" for c in session.settings.file.calls)


def test_checkpoint_undo_via_session_methods(tmp_path):
    session = _elbow_session()
    enable_resilient_mode(session, _config(tmp_path))
    session.checkpoint(
        "pre",
        kind=CheckpointKind.SETTINGS,
        paths=["setup.models.energy.enabled"],
    )
    session._settings_service.set_var("setup.models.energy.enabled", True)
    assert session.settings.setup.models.energy.enabled.get_state() is True
    session.undo()
    assert session.settings.setup.models.energy.enabled.get_state() is False


def test_hard_error_raises_through_interceptor(tmp_path):
    session = _elbow_session()
    enable_resilient_mode(session, _config(tmp_path))
    # A read-only leaf -> hard error -> UnrecoverableStepError.
    session.settings.setup.ro = FakeLeaf("x", read_only=True)

    def reject(value):
        raise RuntimeError("Object is read-only")

    session.settings.setup.ro._set_raises = reject
    with pytest.raises(UnrecoverableStepError):
        session._settings_service.set_var("setup.ro", "y")


def test_transparent_delegation_of_other_methods(tmp_path):
    session = _elbow_session()
    enable_resilient_mode(session, _config(tmp_path))
    # Non-intercepted methods pass straight through to the inner service.
    assert session._settings_service.is_wildcard("x") is False
    assert session._settings_service.get_var("setup.models.energy.enabled") is False


class _Iterate:
    def __init__(self):
        self.count = 0

    def __call__(self, iter_count=0, **kwargs):
        self.count += iter_count
        return {"iterated": iter_count}


def test_scheme_path_resolution():
    # Fluent's service layer uses scheme paths (slashes, hyphens). The resolver
    # must map them to the live tree using each object's fluent_name metadata.
    from ansys.fluent.core.resilient import _compat

    class NamedChild(FakeGroup):
        fluent_name = "cold-inlet"

    class BCs:
        child_names = []

        def __init__(self):
            self._inst = {"cold-inlet": NamedChild(value=FakeLeaf(7))}

        def __getitem__(self, key):
            return self._inst[key]

    bcs = BCs()
    bcs.fluent_name = "boundary-conditions"
    setup = FakeGroup(boundary_conditions=bcs)
    setup.boundary_conditions.fluent_name = "boundary-conditions"

    class Root(FakeGroup):
        child_names = ["setup"]

    root = Root(setup=setup)
    root.setup.fluent_name = "setup"
    bcs.child_names = []
    session = FakeSession(settings=FakeSettings(setup=setup))
    # Point child_names so _child_by_fluent_name can find 'setup'.
    session.settings.child_names = ["setup"]
    setup.child_names = ["boundary_conditions"]

    obj = _compat.resolve_scheme_path(
        session, "setup/boundary-conditions/cold-inlet/value"
    )
    assert obj.get_state() == 7
