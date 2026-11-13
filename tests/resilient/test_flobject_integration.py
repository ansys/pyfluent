# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Resilient mode through PyFluent's real settings objects (no Fluent needed)."""

from pathlib import Path

from _flobject_model import ModelAdapter, ModelSession
import pytest

from ansys.fluent.core.module_config import config
from ansys.fluent.core.resilient.engine import (
    CheckpointConfig,
    EventKind,
    PoolConfig,
    ResilientConfig,
    ResilientFailoverWarning,
    enable_resilient_mode,
)
from ansys.fluent.core.solver.flobject import InactiveObjectError

pytestmark = pytest.mark.resilient


@pytest.fixture(autouse=True)
def _runtime_settings_classes(monkeypatch):
    monkeypatch.setattr(config, "use_runtime_python_classes", True)


def _resilient(tmp_path, **options):
    session = ModelSession()
    enable_resilient_mode(
        session,
        ResilientConfig(checkpoint=CheckpointConfig(directory=tmp_path), **options),
        adapter=ModelAdapter(),
        journal_complete=True,
    )
    events = []
    session.resilient.on_event(events.append)
    return session, events


def test_crash_fails_over_while_navigating_the_settings_tree(tmp_path):
    session, events = _resilient(
        tmp_path, pool=PoolConfig(size=2, launcher=ModelSession)
    )
    inlet = session.settings.bc.inlet
    inlet.intensity = 0.3
    session.crash()
    # Navigation reads attributes of the dead server before anything is written.
    with pytest.warns(ResilientFailoverWarning):
        session.settings.bc.inlet.intensity = 0.4
    standby = session.resilient.active_session
    assert standby is not session
    assert standby.server.objs["bc"].objs["inlet"].objs["intensity"].value == 0.4
    # Objects created before the crash keep working.
    assert inlet.intensity() == 0.4
    assert [e.kind for e in events] == [EventKind.FAILOVER]


def test_inactive_navigation_raises_without_resilient_mode():
    session = ModelSession()
    with pytest.raises(InactiveObjectError):
        session.settings.bc.inlet.thermal.temperature


def test_inactive_navigation_raises_with_resilient_mode(tmp_path):
    # Resilient mode never activates a governing model: an inactive object
    # raises the usual error, whether reading or writing.
    session, events = _resilient(tmp_path)
    with pytest.raises(InactiveObjectError):
        session.settings.bc.inlet.thermal.temperature
    with pytest.raises(InactiveObjectError):
        session.settings.bc.inlet.thermal.temperature = 350.0
    assert session.settings.setup.models.energy.enabled() is False
    assert events == []


def test_rejected_value_keeps_the_usual_error(tmp_path):
    # An out-of-range value raises the original error unchanged.
    session, events = _resilient(tmp_path)
    with pytest.raises(RuntimeError, match="not in range"):
        session.settings.bc.inlet.intensity = 5.0
    assert session.settings.bc.inlet.intensity() == 0.05
    assert events == []


def test_disallowed_value_keeps_the_usual_settings_error(tmp_path):
    # The settings tree reports a disallowed value as a ValueError listing the
    # closest allowed values, exactly as without resilient mode.
    session, _ = _resilient(tmp_path)
    with pytest.raises(ValueError, match="most similar names"):
        session.settings.bc.inlet.specification = "Intensity and Hydraulic Diamete"


def test_failed_solve_is_rolled_back_to_the_automatic_checkpoint(tmp_path):
    session, events = _resilient(tmp_path)
    session.server.diverge = True
    with pytest.raises(RuntimeError, match="Divergence"):
        session.settings.iterate(iter_count=5)
    assert session.settings.bc.inlet.intensity() == 0.05
    assert [e.kind for e in events] == [EventKind.CHECKPOINT, EventKind.ROLLBACK]
    assert Path(session.resilient.checkpoints[-1].path).is_file()


def test_hyphenated_command_names_are_recognized_as_irreversible(tmp_path):
    session, _ = _resilient(tmp_path)
    case = tmp_path / "case.json"
    session.settings.file.write_case(file_name=str(case))
    session.settings.file.read_case(file_name=str(case))
    assert [c.name for c in session.resilient.checkpoints] == ["auto-read_case"]
    commands = [op.command for op in session.resilient.journal.operations]
    assert commands == ["write-case", "read-case"]


def test_undo_through_the_settings_tree(tmp_path):
    session, _ = _resilient(tmp_path)
    session.settings.setup.models.energy.enabled = True
    session.resilient.undo()
    assert session.settings.setup.models.energy.enabled() is False
    session.resilient.redo()
    assert session.settings.setup.models.energy.enabled() is True


def test_disable_restores_plain_settings_behavior(tmp_path):
    session, _ = _resilient(tmp_path)
    session.resilient.disable()
    with pytest.raises(InactiveObjectError):
        session.settings.bc.inlet.thermal.temperature
    with pytest.raises(RuntimeError, match="not in range"):
        session.settings.bc.inlet.intensity = 5.0
