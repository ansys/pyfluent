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

"""Resilient mode against a live Fluent solver (standalone only)."""

import contextlib
from pathlib import Path
import subprocess

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.resilient import (
    CheckpointConfig,
    EventKind,
    PoolConfig,
    ResilientConfig,
    ResilientFailoverWarning,
    ResilientRecoveryWarning,
    enable_resilient_mode,
)

pytestmark = [pytest.mark.resilient, pytest.mark.standalone]


@pytest.fixture
def resilient_elbow(new_solver_session, tmp_path):
    solver = new_solver_session
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    enable_resilient_mode(
        solver,
        ResilientConfig(
            allow_model_activation=True,
            checkpoint=CheckpointConfig(directory=tmp_path),
        ),
    )
    events = []
    solver.resilient.on_event(events.append)
    yield solver, events
    solver.resilient.disable()


def _cold_inlet(solver):
    return solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]


def test_out_of_range_value_is_clamped(resilient_elbow):
    solver, events = resilient_elbow
    turbulence = _cold_inlet(solver).turbulence
    with pytest.warns(ResilientRecoveryWarning):
        turbulence.turbulent_intensity = 5.0
    assert turbulence.turbulent_intensity() == pytest.approx(1.0)
    assert solver.resilient.last_outcome.fixes_applied == ["clamp"]
    assert events[-1].kind is EventKind.RECOVERED


def test_close_typo_is_snapped_to_an_allowed_value(resilient_elbow):
    solver, _ = resilient_elbow
    turbulence = _cold_inlet(solver).turbulence
    target = turbulence.turbulence_specification.allowed_values()[-1]
    with pytest.warns(ResilientRecoveryWarning):
        turbulence.turbulence_specification = target[:-1]
    assert turbulence.turbulence_specification() == target


def test_writing_a_thermal_setting_enables_energy(resilient_elbow):
    solver, events = resilient_elbow
    solver.settings.setup.models.energy.enabled = False
    thermal = _cold_inlet(solver).thermal
    with pytest.warns(ResilientRecoveryWarning, match="energy"):
        thermal.temperature.value = 293.15
    assert solver.settings.setup.models.energy.enabled() is True
    assert thermal.temperature.value() == pytest.approx(293.15)
    assert events[-1].kind is EventKind.ACTIVATED


def test_reading_a_thermal_setting_does_not_enable_energy(resilient_elbow):
    solver, _ = resilient_elbow
    solver.settings.setup.models.energy.enabled = False
    with pytest.raises(RuntimeError, match="inactive"):
        _cold_inlet(solver).thermal.temperature.value()
    assert solver.settings.setup.models.energy.enabled() is False


def test_checkpoint_rollback_and_automatic_checkpoint(resilient_elbow):
    solver, _ = resilient_elbow
    solver.settings.solution.initialization.hybrid_initialize()
    checkpoint = solver.resilient.checkpoint("initialized")
    assert Path(checkpoint.path).is_file()
    solver.settings.solution.run_calculation.iterate(iter_count=2)
    assert solver.resilient.checkpoints[-1].name == "auto-iterate"
    solver.resilient.rollback("initialized")
    assert [c.name for c in solver.resilient.checkpoints] == ["initialized"]


def test_failover_after_the_fluent_process_is_killed(new_solver_session, tmp_path):
    solver = new_solver_session
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    # The standby is launched with the same arguments as the active session.
    enable_resilient_mode(
        solver,
        ResilientConfig(
            checkpoint=CheckpointConfig(directory=tmp_path),
            pool=PoolConfig(size=2),
        ),
    )
    events = []
    solver.resilient.on_event(events.append)
    solver.resilient.checkpoint("before-crash")
    velocity = _cold_inlet(solver).momentum.velocity_magnitude
    velocity.value = 0.5
    # On Windows, Fluent's cleanup script can report a failure even though it
    # killed Fluent.
    with contextlib.suppress(subprocess.CalledProcessError):
        solver.force_exit()
    with pytest.warns(ResilientFailoverWarning):
        _cold_inlet(solver).turbulence.turbulent_intensity = 0.1
    assert solver.resilient.active_session is not solver
    assert EventKind.FAILOVER in [e.kind for e in events]
    # The write made after the checkpoint was replayed onto the standby.
    assert velocity.value() == pytest.approx(0.5)
    assert _cold_inlet(solver).turbulence.turbulent_intensity() == pytest.approx(0.1)
