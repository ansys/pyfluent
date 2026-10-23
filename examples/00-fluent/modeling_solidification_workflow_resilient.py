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

""".. _Solidification_Simulation_Resilient:

Modeling Solidification (resilient mode)
----------------------------------------
This is the :ref:`solidification workflow <Solidification_Simulation>` run in
**resilient mode**. The code is the same ordinary PyFluent code; the only change
is ``resilient_mode=True`` at launch, plus a couple of ``checkpoint`` / ``undo``
calls around the risky transient solve.

**The error this recovers from.** Running the standard example to completion, the
transient ``calculate()`` that advances the solution to ``t = 5 s`` *diverges*:
the residuals blow up (``continuity ~1e+64``), Fluent reports
``Divergence detected in AMG solver`` and then raises a ``floating point
exception``. In the standard example this is an unhandled ``RuntimeError`` that
aborts the whole script -- you lose the converged steady state and the first
transient step too.

**How resilient mode handles it.** Resilient mode:

* auto-checkpoints before every irreversible solve (``calculate`` / ``iterate``),
  and we also take an explicit checkpoint after the good first transient step;
* classifies the ``floating point exception`` as a *non-catastrophic* solver
  error -- the session is still alive, so there is **no** failover and **no** new
  Fluent session; it surfaces as an :class:`UnrecoverableStepError`;
* lets us ``undo()`` back to the last converged state and retry the transient
  advance with **stabilized settings** (smaller time step, stronger
  under-relaxation) instead of discarding the whole run.

This is the key distinction: a diverging solve is *recoverable* (roll back and
re-run), not *catastrophic* (crash and restart). Resilient mode preserves the
expensive converged state so the retry starts from there. Note that resilient mode
owns the *mechanics* of recovery (detect, keep the session alive, restore the good
state); whether the re-run then physically converges still depends on the solver
settings the engineer chooses.
"""

# %%
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.resilient import last_outcome
from ansys.fluent.core.resilient.exceptions import UnrecoverableStepError
from ansys.fluent.core.solver import (
    BoundaryConditions,
    Controls,
    General,
    Initialization,
    Materials,
    Methods,
    Results,
    Setup,
    Solution,
    VelocityInlet,
)

# %%
# Launch Fluent in resilient mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The only difference from the standard example is ``resilient_mode=True``.
solver = pyfluent.launch_fluent(
    precision=pyfluent.Precision.DOUBLE,
    mode="solver",
    dimension=pyfluent.Dimension.TWO,
    resilient_mode=True,
)

# %%
# Read mesh
# ~~~~~~~~~
mesh_file = examples.download_file(
    "solid.msh",
    "pyfluent/solidification",
    save_path=os.getcwd(),
)
solver.settings.file.read_mesh(file_name=mesh_file)

# %%
# Configure solver
# ~~~~~~~~~~~~~~~~
solver_general_settings = General(solver)
solver_general_settings.solver.two_dim_space = "swirl"
solver_general_settings.operating_conditions.gravity = {
    "enable": True,
    "components": [-9.81],
}

# %%
# Enable models (energy is auto-enabled with solidification)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
setup = Setup(solver)
setup.models.viscous.model = "laminar"
solver.tui.define.models.solidification_melting(
    "yes", "constant", "100000", "yes", "no"
)

# %%
# Define material
# ~~~~~~~~~~~~~~~
materials = Materials(solver)
materials.database.copy_by_name(type="fluid", name="air", new_name="liquid-metal")
materials.fluid["liquid-metal"] = {
    "density": {
        "polynomial": {
            "coefficients": [8000, -0.1],
            "function_of": "temperature",
        },
        "option": "polynomial",
    },
    "viscosity": {"value": 0.00553},
    "specific_heat": {"value": 680.0},
    "thermal_conductivity": {"value": 30.0},
    "melting_heat": {"value": 100000.0},
    "tsolidus": {"value": 1150.0},
    "tliqidus": {"value": 1150.0},
}
setup.cell_zone_conditions.fluid["fluid"] = {"general": {"material": "liquid-metal"}}

# %%
# Boundary conditions
# ~~~~~~~~~~~~~~~~~~~
inlet = VelocityInlet(solver, name="inlet")
inlet.momentum.velocity_magnitude.value = 0.00101
inlet.thermal.temperature.value = 1300

outlet = VelocityInlet(solver, name="outlet")
outlet.momentum.velocity_specification_method = "Components"
outlet.momentum.swirl_angular_velocity = 1
outlet.momentum.velocity_components = [0.001, 0, 0]
outlet.thermal.temperature.value = 500

conditions = BoundaryConditions(solver)
conditions.wall["bottom-wall"] = {
    "thermal": {"thermal_condition": "Temperature", "temperature": 1300}
}
conditions.wall["free-surface"] = {
    "momentum": {
        "shear_condition": "Marangoni Stress",
        "surface_tension_gradient": -0.00036,
    },
    "thermal": {
        "thermal_condition": "Convection",
        "free_stream_temp": 1500,
        "heat_transfer_coeff": 100,
    },
}
conditions.wall["side-wall"] = {
    "thermal": {"thermal_condition": "Temperature", "temperature": 1400}
}
conditions.wall["solid-wall"] = {
    "momentum": {
        "wall_motion": "Moving Wall",
        "velocity_spec": "Rotational",
        "rotation_speed": 1,
    },
    "thermal": {"thermal_condition": "Temperature", "temperature": 500},
}

# %%
# Solution methods
# ~~~~~~~~~~~~~~~~
methods = Methods(solver)
methods.p_v_coupling.flow_scheme = "Coupled"
methods.spatial_discretization.discretization_scheme = {"pressure": "presto!"}
methods.pseudo_time_method.formulation = {"coupled_solver": "global-time-step"}

# %%
# Steady conduction solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
controls = Controls(solver)
controls.equations = {"flow": False, "w-swirl": False}

initialize = Initialization(solver)
initialize.hybrid_initialize()

results = Results(solver)
results.custom_field_functions.create(
    name="omegar", custom_field_function="1 * radial_coordinate"
)
initialize.patch.calculate_patch(
    cell_zones=["fluid"],
    variable="x-pull-velocity",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=True,
    custom_field_function_name="omegar",
    value=0.001,
)
initialize.patch.calculate_patch(
    cell_zones=["fluid"],
    variable="z-pull-velocity",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=True,
    custom_field_function_name="omegar",
)
solver.settings.solution.run_calculation.pseudo_time_settings.time_step_method = {
    "time_step_method": "user-specified",
    "auto_time_size_calc_solid_zone": False,
}

solver.settings.solution.run_calculation.iterate(iter_count=20)

# %%
# Enable transient flow and heat transfer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
solver_general_settings.solver.time = "unsteady-1st-order"
controls.equations = {"flow": True, "w-swirl": True}
controls.under_relaxation = {"delh": 0.1}

solutions = Solution(solver)

# %%
# First transient step (converges), then checkpoint the good state
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
solutions.run_calculation.transient_controls.time_step_count = 2
solutions.run_calculation.transient_controls.time_step_size = 0.1
solutions.run_calculation.calculate()

# Explicit checkpoint of the last known-good converged state.
solver.checkpoint("converged-t0p2")

# %%
# Continue the transient solve -- this is the step that diverges
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Resilient mode auto-checkpoints before this ``calculate`` as well. If the solve
# diverges (floating point exception), it is a *non-catastrophic* error: the
# session stays alive, so we roll back and retry with stabilized settings instead
# of losing the whole run.
solutions.run_calculation.transient_controls.time_step_count = 48


def advance_transient():
    """Advance the transient solution, returning True on success."""
    try:
        solutions.run_calculation.calculate()
        return True
    except UnrecoverableStepError as err:
        # Non-catastrophic solver divergence: the session is still usable.
        print(f"Transient solve failed (recoverable): {err}")
        return False


if not advance_transient():
    # %%
    # Recover: roll back to the converged state and retry, stabilized
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("Rolling back to the last converged checkpoint and stabilizing...")
    solver.rewind_to("converged-t0p2")

    # Stabilize: a much smaller time step and stronger under-relaxation make the
    # transient advance robust after the divergence. We also take only a few
    # steps so the retry completes quickly; a production run would continue from
    # this stabilized, converged state.
    controls.under_relaxation = {"delh": 0.02}
    solutions.run_calculation.transient_controls.time_step_size = 0.001
    solutions.run_calculation.transient_controls.time_step_count = 5

    if advance_transient():
        print("Transient solve converged after resilient recovery.")
    else:
        # The run is still usable and sitting at the preserved converged state;
        # a production script would try further stabilization (ramped controls,
        # smaller steps) from here. The key point is that nothing was lost.
        print(
            "Still diverging with these settings -- but the session is alive and "
            "restored to the converged checkpoint, ready for another attempt."
        )
else:
    print("Transient solve converged on the first attempt.")

# %%
# Inspect the outcome of the last resilient operation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("last resilient outcome:", last_outcome(solver))

# %%
# Save and close
# ~~~~~~~~~~~~~~
solver.settings.file.write_case_data(file_name="solidification_resilient")
solver.exit()

# %%
# Summary
# ~~~~~~~
#
# Resilient mode turned an unrecoverable crash into a recoverable event. The
# diverging transient ``calculate()`` raised a ``floating point exception``, which
# resilient mode classified as *non-catastrophic* (the session stayed alive, so no
# failover and no new Fluent session). Because resilient mode had checkpointed the
# converged state, we rolled back with ``rewind_to`` and re-ran the transient
# advance from that preserved state -- instead of losing the expensive steady-state
# and first transient results and starting over.
#
# Two responsibilities are cleanly separated here. Resilient mode guarantees the
# *mechanics* of recovery: it detects that the solver error is non-catastrophic,
# keeps the session alive, and restores the last good state on demand. Whether the
# retry then *physically converges* is the engineer's domain -- it depends on the
# solver settings chosen for the re-run (time step, under-relaxation, ramping).
# Resilient mode's job is to make sure a bad attempt never costs you the good state
# you already paid for.
