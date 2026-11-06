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

* repairs rejected values and enables a governing model when needed,
* undoes and redoes settings writes,
* checkpoints before ``iterate`` and rolls back on request.

See :ref:`ref_resilient_guide` for details.
"""

# %%
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.resilient import ResilientConfig

import_file_name = examples.download_file(
    "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
)

# %%
# Launch Fluent in resilient mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ``allow_model_activation=True`` lets resilient mode enable a governing model,
# such as energy, when you write a setting that depends on it.

solver = pyfluent.launch_fluent(
    precision=pyfluent.Precision.DOUBLE,
    processor_count=2,
    mode=pyfluent.FluentMode.SOLVER,
    resilient_mode=True,
    resilient_config=ResilientConfig(allow_model_activation=True),
)
solver.resilient.on_event(lambda event: print(f"[{event.kind.value}] {event.message}"))

# %%
# Read the mesh
# ~~~~~~~~~~~~~

solver.settings.file.read_mesh(file_name=import_file_name)

# %%
# Set up boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# The energy model is off, so the inlet temperature is inactive. Writing it
# enables the energy model first. The turbulent intensity of 5 is outside the
# allowed range and is clamped to the upper bound with a warning.

cold_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
cold_inlet.momentum.velocity_magnitude.value = 0.4
cold_inlet.turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
cold_inlet.turbulence.turbulent_intensity = 5
cold_inlet.turbulence.hydraulic_diameter = "4 [in]"
cold_inlet.thermal.temperature.value = 293.15

print("energy enabled:", solver.settings.setup.models.energy.enabled())
print("turbulent intensity:", cold_inlet.turbulence.turbulent_intensity())

hot_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["hot-inlet"]
hot_inlet.momentum.velocity_magnitude.value = 1.2
hot_inlet.turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
hot_inlet.turbulence.hydraulic_diameter = "1 [in]"
hot_inlet.thermal.temperature.value = 313.15

# %%
# Undo and redo a settings change
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

cold_inlet.turbulence.turbulent_intensity = 0.05
solver.resilient.undo()
print("after undo:", cold_inlet.turbulence.turbulent_intensity())
solver.resilient.redo()
print("after redo:", cold_inlet.turbulence.turbulent_intensity())

# %%
# Initialize and checkpoint
# ~~~~~~~~~~~~~~~~~~~~~~~~~

solver.settings.solution.initialization.hybrid_initialize()
solver.resilient.checkpoint("initialized")

# %%
# Solve
# ~~~~~
# ``iterate`` is irreversible, so resilient mode writes an automatic checkpoint
# before it runs. If the solve failed, the session would be restored to that
# checkpoint and the error raised.

solver.settings.solution.run_calculation.iterate(iter_count=100)
print("checkpoints:", [checkpoint.name for checkpoint in solver.resilient.checkpoints])

# %%
# Roll back to the initialized state
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver.resilient.rollback("initialized")

# %%
# Exit
# ~~~~

solver.exit()
