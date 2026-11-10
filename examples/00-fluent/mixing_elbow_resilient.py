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

""".. _ref_mixing_elbow_resilient:

Mixing elbow in resilient mode
------------------------------
This example sets up and solves the mixing elbow with ordinary settings API
code, launched with ``resilient_mode=True``. It shows how resilient mode:

* undoes and redoes settings writes,
* checkpoints before ``iterate`` and rolls back on request.

See :ref:`ref_resilient_guide` for details.
"""

# %%
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_file_name = examples.download_file(
    "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
)

# %%
# Launch Fluent in resilient mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver_session = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.DOUBLE,
    processor_count=2,
    resilient_mode=True,
)
resilient = solver_session.resilient
resilient.on_event(lambda event: print(f"[{event.kind.value}] {event.message}"))

# %%
# Read the mesh
# ~~~~~~~~~~~~~

solver_session.settings.file.read_mesh(file_name=import_file_name)

# %%
# Set up boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

# Built-in solver objects:
energy = pyfluent.solver.Energy(settings_source=solver_session)
cold_inlet = pyfluent.solver.VelocityInlet(
    settings_source=solver_session, name="cold-inlet"
)
hot_inlet = pyfluent.solver.VelocityInlet(
    settings_source=solver_session, name="hot-inlet"
)
# Aliasing reused objects:
cold_turbulence = cold_inlet.turbulence
turbulent_intensity = cold_turbulence.turbulent_intensity
hot_turbulence = hot_inlet.turbulence

energy.enabled = True
cold_inlet.momentum.velocity_magnitude.value = 0.4
cold_turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
turbulent_intensity.set_state(0.05)
cold_turbulence.hydraulic_diameter = "4 [in]"
cold_inlet.thermal.temperature.value = 293.15

hot_inlet.momentum.velocity_magnitude.value = 1.2
hot_turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
hot_turbulence.hydraulic_diameter = "1 [in]"
hot_inlet.thermal.temperature.value = 313.15

# %%
# Undo and redo a settings change
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Try a higher turbulent intensity at the cold inlet. Undo restores the 0.05 set
# above, and redo applies 0.1 again. A second undo keeps the setup at 0.05 for
# the solve.

turbulent_intensity.set_state(0.1)
print("changed:", turbulent_intensity())
resilient.undo()
print("after undo:", turbulent_intensity())
resilient.redo()
print("after redo:", turbulent_intensity())
resilient.undo()
print("after a second undo:", turbulent_intensity())

# %%
# Initialize and checkpoint
# ~~~~~~~~~~~~~~~~~~~~~~~~~

initialization = pyfluent.solver.Initialization(settings_source=solver_session)
initialization.hybrid_initialize()
resilient.checkpoint("initialized")

# %%
# Solve
# ~~~~~
# ``iterate`` is irreversible, so resilient mode writes an automatic checkpoint
# before it runs. If the solve failed, the session would be restored to that
# checkpoint and the error raised.

run_calculation = pyfluent.solver.RunCalculation(settings_source=solver_session)
run_calculation.iterate(iter_count=100)
print("checkpoints:", [checkpoint.name for checkpoint in resilient.checkpoints])

# %%
# Roll back to the initialized state
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

resilient.rollback("initialized")

# %%
# Exit
# ~~~~

solver_session.exit()
