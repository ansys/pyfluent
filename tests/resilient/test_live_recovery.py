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

"""Live (standalone) integration tests for resilient-mode auto-recovery.

These require a real Fluent and are skipped unless the standalone suite is run.
They exercise the recovery paths end to end against a live solver, using ordinary
PyFluent code -- confirming the behaviour verified manually on Fluent 27.1.0:

* out-of-range value -> clamped to the live ``[min, max]``;
* disallowed enum value -> snapped to the nearest live ``allowed_values`` entry;
* inactive target (thermal BC with energy off) -> governing model discovered and
  enabled automatically.

Run with, for example::

    pytest tests/resilient/test_live_recovery.py -m "resilient and standalone"
"""

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.resilient import enable_resilient_mode, last_outcome

pytestmark = [pytest.mark.resilient, pytest.mark.standalone]


@pytest.fixture
def resilient_mixing_elbow(new_solver_session):
    """A resilient-mode solver with the mixing-elbow case loaded."""
    solver = new_solver_session
    enable_resilient_mode(solver)
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    solver.settings.setup.models.energy.enabled = True
    return solver


def test_out_of_range_auto_clamped_live(resilient_mixing_elbow):
    solver = resilient_mixing_elbow
    cold = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    # Turbulent intensity must be in [0, 1]; 5.0 is out of range.
    cold.turbulence.turbulent_intensity = 5.0
    out = last_outcome(solver)
    assert out is not None and out.ok
    assert "clamp" in out.fixes_applied
    # Live value clamped to the maximum.
    assert cold.turbulence.turbulent_intensity() == pytest.approx(1.0)


def test_disallowed_value_snapped_live(resilient_mixing_elbow):
    solver = resilient_mixing_elbow
    cold = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    spec = cold.turbulence.turbulence_specification
    allowed = spec.allowed_values()
    assert allowed, "expected a non-empty allowed-values list"
    # A near-miss of a real allowed value (drop the trailing char).
    target = allowed[-1]
    typo = target[:-1]
    cold.turbulence.turbulence_specification = typo
    out = last_outcome(solver)
    assert out is not None and out.ok
    assert "nearest_allowed" in out.fixes_applied
    assert cold.turbulence.turbulence_specification() == target


def test_inactive_thermal_activates_energy_live(new_solver_session):
    solver = new_solver_session
    enable_resilient_mode(solver)
    case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case(file_name=case)
    # Ensure energy is OFF, so the thermal BC is inactive.
    solver.settings.setup.models.energy.enabled = False
    cold = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    # Setting the thermal temperature must auto-discover and enable energy.
    cold.thermal.temperature.value = 293.15
    assert solver.settings.setup.models.energy.enabled() is True
    assert cold.thermal.temperature.value() == pytest.approx(293.15)
