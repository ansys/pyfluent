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

import ansys.fluent.core as pyfluent
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
    return pyfluent.solver.VelocityInlet(settings_source=solver, name="cold-inlet")


def test_rejected_value_raises_the_original_error_unchanged(resilient_elbow):
    # Resilient mode never changes a value to make a rejected write succeed.
    solver, events = resilient_elbow
    inlet_turbulence = _cold_inlet(solver).turbulence
    turbulent_intensity = inlet_turbulence.turbulent_intensity
    inlet_turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
    before = turbulent_intensity()
    with pytest.raises(RuntimeError):
        turbulent_intensity.set_state(5.0)
    assert turbulent_intensity() == pytest.approx(before)
    assert events == []


def test_writing_an_inactive_setting_raises(resilient_elbow):
    # The energy model is off, so the inlet temperature is inactive. Resilient
    # mode does not enable the model; the usual error is raised.
    solver, events = resilient_elbow
    energy = pyfluent.solver.Energy(settings_source=solver)
    energy.enabled = False
    with pytest.raises(RuntimeError, match="inactive"):
        _cold_inlet(solver).thermal.temperature.value = 293.15
    assert energy.enabled() is False


def test_checkpoint_rollback_and_automatic_checkpoint(resilient_elbow):
    solver, _ = resilient_elbow
    resilient = solver.resilient
    pyfluent.solver.Initialization(settings_source=solver).hybrid_initialize()
    checkpoint = resilient.checkpoint("initialized")
    assert Path(checkpoint.path).is_file()
    pyfluent.solver.RunCalculation(settings_source=solver).iterate(iter_count=2)
    assert resilient.checkpoints[-1].name == "auto-iterate"
    resilient.rollback("initialized")
    assert [c.name for c in resilient.checkpoints] == ["initialized"]


def test_failover_after_the_fluent_process_is_killed(new_solver_session, tmp_path):
    solver = new_solver_session
    # As resilient_mode=True does at launch. The standby is launched with the
    # same arguments as the active session.
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
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    cold_inlet = _cold_inlet(solver)
    velocity = cold_inlet.momentum.velocity_magnitude
    turbulent_intensity = cold_inlet.turbulence.turbulent_intensity
    velocity.value = 0.5
    # The standby read the case and applied the write too.
    assert solver.resilient.wait_for_standbys(timeout=300)
    (standby,) = solver.resilient.pool.standbys
    standby_velocity = _cold_inlet(standby).momentum.velocity_magnitude
    assert standby_velocity.value() == pytest.approx(0.5)
    # On Windows, Fluent's cleanup script can report a failure even though it
    # killed Fluent.
    with contextlib.suppress(subprocess.CalledProcessError):
        solver.force_exit()
    # The next call fails over. A read is repeated on the standby.
    with pytest.warns(ResilientFailoverWarning):
        assert velocity.value() == pytest.approx(0.5)
    assert solver.resilient.active_session is standby
    assert EventKind.FAILOVER in [e.kind for e in events]
    # The standby now serves new writes.
    turbulent_intensity.set_state(0.1)
    assert turbulent_intensity() == pytest.approx(0.1)


def test_solution_data_survives_the_fluent_process_being_killed(
    new_solver_session, tmp_path
):
    # Like the failover test, but with a solve: the standby runs the same solve,
    # so the session that takes over holds the solution, not just the settings.
    solver = new_solver_session
    _enable_on_new_session(
        solver,
        ResilientConfig(
            checkpoint=CheckpointConfig(directory=tmp_path),
            pool=PoolConfig(size=2),
        ),
        launched=True,
    )
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    turbulent_intensity = _cold_inlet(solver).turbulence.turbulent_intensity
    pyfluent.solver.Initialization(settings_source=solver).hybrid_initialize()
    pyfluent.solver.RunCalculation(settings_source=solver).iterate(iter_count=20)
    assert _data_is_valid(solver)
    assert solver.resilient.wait_for_standbys(timeout=600)
    (standby,) = solver.resilient.pool.standbys
    assert _data_is_valid(standby)

    # Kill Fluent, then trigger failover with a read on the main thread.
    # On Windows, Fluent's cleanup script can report a failure even though it
    # killed Fluent.
    with contextlib.suppress(subprocess.CalledProcessError):
        solver.force_exit()
    with pytest.warns(ResilientFailoverWarning):
        turbulent_intensity()
    # Services other than settings are reached through the session that is now
    # serving.
    assert solver.resilient.active_session is standby
    assert _data_is_valid(solver.resilient.active_session)


def test_solution_data_survives_a_kill_during_iteration(new_solver_session, tmp_path):
    # Fluent is killed while it iterates. The interrupted solve is not repeated
    # on the standby, which takes over with the solution of the previous solve.
    solver = new_solver_session
    _enable_on_new_session(
        solver,
        ResilientConfig(
            # Start iterating at once, so that the kill lands during the solve
            # rather than during the automatic checkpoint before it.
            auto_checkpoint=False,
            checkpoint=CheckpointConfig(directory=tmp_path),
            pool=PoolConfig(size=2),
        ),
        launched=True,
    )
    events = []
    solver.resilient.on_event(events.append)
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    run_calculation = pyfluent.solver.RunCalculation(settings_source=solver)
    pyfluent.solver.Initialization(settings_source=solver).hybrid_initialize()
    run_calculation.iterate(iter_count=20)
    assert solver.resilient.wait_for_standbys(timeout=600)
    (standby,) = solver.resilient.pool.standbys
    assert _data_is_valid(standby)

    errors = []

    def long_solve():
        try:
            run_calculation.iterate(iter_count=5000)
        except Exception as err:  # noqa: BLE001
            errors.append(err)

    worker = threading.Thread(target=long_solve)
    worker.start()
    time.sleep(3)
    assert worker.is_alive(), "The solve ended before Fluent was killed."
    # On Windows, Fluent's cleanup script can report a failure even though it
    # killed Fluent.
    with contextlib.suppress(subprocess.CalledProcessError):
        solver.force_exit()
    worker.join(timeout=300)
    assert not worker.is_alive()

    # The solve failed over to the standby, raised its error, and was not
    # repeated there.
    (error,) = errors
    assert "not repeated" in " ".join(getattr(error, "__notes__", []))
    assert solver.resilient.active_session is standby
    assert solver.resilient.last_outcome.failed_over
    assert EventKind.FAILOVER in [e.kind for e in events]
    # The standby holds the solution of the first solve and serves new calls.
    assert _data_is_valid(standby)
    turbulent_intensity = _cold_inlet(solver).turbulence.turbulent_intensity
    turbulent_intensity.set_state(0.1)
    assert turbulent_intensity() == pytest.approx(0.1)


def _data_is_valid(solver) -> bool:
    """Whether the active session currently holds valid solution data."""
    # (data-valid?) is the scheme flag resilient mode itself uses to decide
    # whether a checkpoint includes data; it is defined in all supported Fluent
    # releases, unlike (iteration-data).
    return solver.scheme.eval("(data-valid?)") is True
