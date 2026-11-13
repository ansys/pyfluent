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

""".. _Solidification_Simulation_Resilient:

Modeling solidification in resilient mode
-----------------------------------------
This example runs the :ref:`solidification workflow <Solidification_Simulation>`
with ``resilient_mode=True``.

Starting the transient solve from the steady solution with a time step of
0.1 s diverges, and Fluent raises a floating point exception. Without resilient
mode, the session is left in the diverged state. In resilient mode, a
checkpoint is written before ``calculate`` runs. When the solve fails, the
session is restored to that checkpoint and the original error is raised, so the
script can catch it, reduce the time step and solve again from the steady
solution.

See :ref:`ref_resilient_guide` for details.
"""

# %%
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

# %%
# Launch Fluent in resilient mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver_session = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.DOUBLE,
    dimension=pyfluent.Dimension.TWO,
    resilient_mode=True,
)
resilient = solver_session.resilient
resilient.on_event(lambda event: print(f"[{event.kind.value}] {event.message}"))

# %%
# Read the mesh
# ~~~~~~~~~~~~~

mesh_file = examples.download_file("solid.msh", "pyfluent/solidification")
solver_session.settings.file.read_mesh(file_name=mesh_file)

# %%
# Configure the solver
# ~~~~~~~~~~~~~~~~~~~~

# Built-in solver objects:
general = pyfluent.solver.General(settings_source=solver_session)
# Aliasing reused objects:
general_solver = general.solver

general_solver.two_dim_space = "swirl"
general.operating_conditions.gravity = {"enable": True, "components": [-9.81]}

# %%
# Enable the models
# ~~~~~~~~~~~~~~~~~
# The energy model is enabled together with solidification and melting.

viscous = pyfluent.solver.Viscous(settings_source=solver_session)
viscous.model = "laminar"
solver_session.tui.define.models.solidification_melting(
    "yes", "constant", "100000", "yes", "no"
)

# %%
# Define the material
# ~~~~~~~~~~~~~~~~~~~

materials = pyfluent.solver.Materials(settings_source=solver_session)
materials.database.copy_by_name(type="fluid", name="air", new_name="liquid-metal")
materials.fluid["liquid-metal"] = {
    "density": {
        "polynomial": {"coefficients": [8000, -0.1], "function_of": "temperature"},
        "option": "polynomial",
    },
    "viscosity": {"value": 0.00553},
    "specific_heat": {"value": 680.0},
    "thermal_conductivity": {"value": 30.0},
    "melting_heat": {"value": 100000.0},
    "tsolidus": {"value": 1150.0},
    "tliqidus": {"value": 1150.0},
}
fluid = pyfluent.solver.FluidCellZone(settings_source=solver_session, name="fluid")
fluid.general.material = "liquid-metal"

# %%
# Set the boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

inlet = pyfluent.solver.VelocityInlet(settings_source=solver_session, name="inlet")
inlet.momentum.velocity_magnitude.value = 0.00101
inlet.thermal.temperature.value = 1300

outlet = pyfluent.solver.VelocityInlet(settings_source=solver_session, name="outlet")
outlet_momentum = outlet.momentum
outlet_momentum.velocity_specification_method = "Components"
outlet_momentum.swirl_angular_velocity = 1
outlet_momentum.velocity_components = [0.001, 0, 0]
outlet.thermal.temperature.value = 500

bottom_wall = pyfluent.solver.WallBoundary(
    settings_source=solver_session, name="bottom-wall"
)
bottom_wall.thermal = {"thermal_condition": "Temperature", "temperature": 1300}

free_surface = pyfluent.solver.WallBoundary(
    settings_source=solver_session, name="free-surface"
)
free_surface.momentum = {
    "shear_condition": "Marangoni Stress",
    "surface_tension_gradient": -0.00036,
}
free_surface.thermal = {
    "thermal_condition": "Convection",
    "free_stream_temp": 1500,
    "heat_transfer_coeff": 100,
}

side_wall = pyfluent.solver.WallBoundary(
    settings_source=solver_session, name="side-wall"
)
side_wall.thermal = {"thermal_condition": "Temperature", "temperature": 1400}

solid_wall = pyfluent.solver.WallBoundary(
    settings_source=solver_session, name="solid-wall"
)
solid_wall.momentum = {
    "wall_motion": "Moving Wall",
    "velocity_spec": "Rotational",
    "rotation_speed": 1,
}
solid_wall.thermal = {"thermal_condition": "Temperature", "temperature": 500}

# %%
# Set the solution methods
# ~~~~~~~~~~~~~~~~~~~~~~~~

methods = pyfluent.solver.Methods(settings_source=solver_session)
methods.p_v_coupling.flow_scheme = "Coupled"
methods.spatial_discretization.discretization_scheme = {"pressure": "presto!"}
methods.pseudo_time_method.formulation = {"coupled_solver": "global-time-step"}

# %%
# Solve the steady conduction problem
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

controls = pyfluent.solver.Controls(settings_source=solver_session)
controls.equations = {"flow": False, "w-swirl": False}

initialization = pyfluent.solver.Initialization(settings_source=solver_session)
initialization.hybrid_initialize()

results = pyfluent.solver.Results(settings_source=solver_session)
results.custom_field_functions.create(
    name="omegar", custom_field_function="1 * radial_coordinate"
)
calculate_patch = initialization.patch.calculate_patch
calculate_patch(
    cell_zones=["fluid"],
    variable="x-pull-velocity",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=True,
    custom_field_function_name="omegar",
    value=0.001,
)
calculate_patch(
    cell_zones=["fluid"],
    variable="z-pull-velocity",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=True,
    custom_field_function_name="omegar",
)

run_calculation = pyfluent.solver.RunCalculation(settings_source=solver_session)
run_calculation.pseudo_time_settings.time_step_method = {
    "time_step_method": "user-specified",
    "auto_time_size_calc_solid_zone": False,
}
run_calculation.iterate(iter_count=20)

# %%
# Solve the transient problem and recover from the divergence
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# With a time step of 0.1 s the solve diverges. Resilient mode restores the
# checkpoint written before ``calculate``, which holds the steady solution, and
# raises the original error. The script then reduces the time step, increases
# the under-relaxation and solves again from the steady solution.

general_solver.time = "unsteady-1st-order"
controls.equations = {"flow": True, "w-swirl": True}
controls.under_relaxation = {"delh": 0.1}

transient_controls = run_calculation.transient_controls
transient_controls.time_step_size = 0.1
transient_controls.time_step_count = 50
try:
    run_calculation.calculate()
except RuntimeError as error:
    print(f"Transient solve failed: {error}")
    print("Rolled back:", resilient.last_outcome.rolled_back)
    controls.under_relaxation = {"delh": 0.02}
    transient_controls.time_step_size = 0.001
    transient_controls.time_step_count = 5
    run_calculation.calculate()

# %%
# Save and exit
# ~~~~~~~~~~~~~

solver_session.settings.file.write_case_data(file_name="solidification_resilient")
solver_session.exit()
