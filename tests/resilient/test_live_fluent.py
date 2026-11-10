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
import threading
import time

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.resilient import (
    CheckpointConfig,
    EventKind,
    PoolConfig,
    ResilientConfig,
    ResilientFailoverWarning,
    _enable_on_new_session,
)

pytestmark = [pytest.mark.resilient, pytest.mark.standalone]


@pytest.fixture
def resilient_elbow(new_solver_session, tmp_path):
    solver = new_solver_session
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    _enable_on_new_session(
        solver,
        ResilientConfig(checkpoint=CheckpointConfig(directory=tmp_path)),
        launched=True,
    )
    events = []
    solver.resilient.on_event(events.append)
    yield solver, events
    solver.resilient.disable()


def _cold_inlet(solver):
    return solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]


def test_rejected_value_raises_the_original_error_unchanged(resilient_elbow):
    # Resilient mode never changes a value to make a rejected write succeed.
    solver, events = resilient_elbow
    turbulence = _cold_inlet(solver).turbulence
    turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
    before = turbulence.turbulent_intensity()
    with pytest.raises(RuntimeError):
        turbulence.turbulent_intensity = 5.0
    assert turbulence.turbulent_intensity() == pytest.approx(before)
    assert events == []


def test_writing_an_inactive_setting_raises(resilient_elbow):
    # The energy model is off, so the inlet temperature is inactive. Resilient
    # mode does not enable the model; the usual error is raised.
    solver, events = resilient_elbow
    solver.settings.setup.models.energy.enabled = False
    with pytest.raises(RuntimeError, match="inactive"):
        _cold_inlet(solver).thermal.temperature.value = 293.15
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
    _enable_on_new_session(
        solver,
        ResilientConfig(
            checkpoint=CheckpointConfig(directory=tmp_path),
            pool=PoolConfig(size=2),
        ),
        launched=True,
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


def test_data_recovery_after_the_fluent_process_is_killed_during_iteration(
    new_solver_session, tmp_path
):
    # Like the failover test, but the active session is killed WHILE iterating.
    # The checkpoint captured the case and its solution data, so the standby that
    # takes over holds the converged solution, not just the settings.
    solver = new_solver_session
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    _enable_on_new_session(
        solver,
        ResilientConfig(
            checkpoint=CheckpointConfig(directory=tmp_path),
            pool=PoolConfig(size=2),
        ),
        launched=True,
    )
    run_calculation = solver.settings.solution.run_calculation
    solver.settings.solution.initialization.hybrid_initialize()
    run_calculation.iterate(iter_count=20)
    # Checkpoint the converged solution (case and data).
    checkpoint = solver.resilient.checkpoint("converged")
    assert checkpoint.include_data
    iterations = _iteration_count(solver)
    assert iterations > 0

    # Kill Fluent during a long iteration run on a background thread.
    def long_run():
        with contextlib.suppress(Exception):
            run_calculation.iterate(iter_count=1000)

    worker = threading.Thread(target=long_run)
    worker.start()
    time.sleep(2)
    with contextlib.suppress(subprocess.CalledProcessError):
        solver.force_exit()
    worker.join(timeout=120)

    # The standby takes over on the next call and holds the checkpointed data.
    with pytest.warns(ResilientFailoverWarning):
        recovered = _iteration_count(solver)
    assert solver.resilient.active_session is not solver
    # The recovered session has the solution data of the checkpoint (iterations
    # were preserved), so it is not an empty, freshly read case.
    assert recovered >= iterations


def _iteration_count(solver) -> int:
    """Return the number of iterations in the current data, or 0."""
    try:
        return int(solver.scheme.eval("(length (iteration-data))"))
    except Exception:  # noqa: BLE001
        # Fall back to a data-validity probe when the scheme call is unavailable.
        return 1 if solver.scheme.eval("(data-valid?)") else 0
