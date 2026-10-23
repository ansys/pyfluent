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

""".. _ref_mixing_elbow_resilient:

Resilient solver setup and solution
-----------------------------------
This example solves the mixing-elbow case exactly like the standard
:ref:`settings-API example <ref_mixing_elbow_settings_api_beta>` -- the PyFluent
code is identical -- but launches with ``resilient_mode=True``. That single flag
makes the ordinary ``solver.settings...`` writes and commands **resilient**:

* **auto-recovery** -- a recoverable Fluent error (for example an out-of-range
  value) is classified, repaired against the live bounds / allowed values, and
  retried automatically, with no special API;
* **two-tier checkpoints with undo** -- the session gains ``checkpoint`` /
  ``undo`` / ``redo``, and irreversible commands (``iterate``, ``read_case``, ...)
  are auto-checkpointed so they can be rolled back;
* **failover** -- if you launch with ``pool_size > 1`` (via ``resilient_config``),
  a fatal solver error fails over to a warm standby and replays the last
  checkpoint instead of cold-restarting.

Note that below the code reads just like normal PyFluent: there is no new
per-call API to learn. Resilience happens transparently inside the settings tree.
"""

###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_file_name = examples.download_file(
    "mixing_elbow.msh.h5",
    "pyfluent/mixing_elbow",
    save_path=os.getcwd(),
)

###############################################################################
# Launch Fluent in resilient mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The only difference from a normal launch is ``resilient_mode=True``. Everything
# after this point is ordinary PyFluent code.

solver = pyfluent.launch_fluent(
    precision="double",
    processor_count=2,
    mode="solver",
    resilient_mode=True,
)

###############################################################################
# Read the mesh and check it
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# ``read_mesh`` is irreversible, so resilient mode takes an automatic file
# checkpoint before it runs.

solver.settings.file.read_mesh(file_name=import_file_name)
solver.settings.mesh.check()

###############################################################################
# Enable heat transfer
# ~~~~~~~~~~~~~~~~~~~~
solver.settings.setup.models.energy.enabled = True

###############################################################################
# Set up boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Exactly as in the standard example. If any value is rejected by Fluent as
# recoverable (for example out of range), resilient mode repairs and retries it
# automatically -- you would otherwise have had to catch the error yourself.

cold_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
cold_inlet.momentum.velocity_magnitude.value = 0.4
cold_inlet.turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
cold_inlet.turbulence.turbulent_intensity = 0.05
cold_inlet.turbulence.hydraulic_diameter = "4 [in]"
cold_inlet.thermal.temperature.value = 293.15

hot_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["hot-inlet"]
hot_inlet.momentum.velocity_magnitude.value = 1.2
hot_inlet.turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
hot_inlet.turbulence.hydraulic_diameter = "1 [in]"
hot_inlet.thermal.temperature.value = 313.15

###############################################################################
# Initialize the flow field
# ~~~~~~~~~~~~~~~~~~~~~~~~~
solver.settings.solution.initialization.hybrid_initialize()

###############################################################################
# Take an explicit checkpoint before solving
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ``checkpoint`` / ``undo`` / ``redo`` are available on the session because it was
# launched in resilient mode. This checkpoint is also the state replayed onto a
# warm standby if the solver hits a fatal error during iteration.

solver.checkpoint("pre-iterate")

###############################################################################
# Solve
# ~~~~~
# ``iterate`` is irreversible; resilient mode auto-checkpoints before it as well.

solver.settings.solution.run_calculation.iterate(iter_count=100)

###############################################################################
# Roll back to the pre-iterate checkpoint
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ``undo`` reloads the case + data captured by the ``pre-iterate`` checkpoint.

solver.undo()

###############################################################################
# Exit
# ~~~~
solver.exit()
