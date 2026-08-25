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

"""Fluent session classes for meshing, solving, and file-based workflows.

Class hierarchy
---------------
The two non-user-facing base classes (``BaseSession``, ``BaseMeshing``) live in
private modules and must not be instantiated directly.  All concrete session
objects are created via :func:`ansys.fluent.core.launch_fluent`.

.. code-block:: text

    BaseSession  (private)
    ├── Solver                — full solver session
    │   ├── SolverAero        — solver + Aero add-on
    │   ├── SolverIcing       — solver + Icing add-on
    │   └── SolverLite        — lightweight solver variant
    │   └── PrePost            — pre-post session
    └── BaseMeshing  (private)   — full public meshing API
        ├── PureMeshing       — meshing-only (no solver switching)
        └── Meshing           — meshing with :meth:`~Meshing.switch_to_solver`

Session aliases
---------------
Each concrete class is re-exported here with a ``Session`` suffix for backward
compatibility and convenience:

- :class:`SolverSession`       → :class:`~ansys.fluent.core.session.solver.Solver`
- :class:`SolverAeroSession`   → :class:`~ansys.fluent.core.session.solver_aero.SolverAero`
- :class:`SolverIcingSession`  → :class:`~ansys.fluent.core.session.solver_icing.SolverIcing`
- :class:`SolverLiteSession`   → :class:`~ansys.fluent.core.session.solver_lite.SolverLite`
- :class:`PureMeshingSession`  → :class:`~ansys.fluent.core.session.pure_meshing.PureMeshing`
- :class:`MeshingSession`      → :class:`~ansys.fluent.core.session.meshing.Meshing`
- :class:`FileSession`         → :class:`~ansys.fluent.core.session.file.FileSession`
"""


from ansys.fluent.core.session.file import FileSession
from ansys.fluent.core.session.meshing import Meshing as MeshingSession
from ansys.fluent.core.session.pure_meshing import PureMeshing as PureMeshingSession
from ansys.fluent.core.session.solver import Solver as SolverSession
from ansys.fluent.core.session.solver_aero import SolverAero as SolverAeroSession
from ansys.fluent.core.session.solver_icing import SolverIcing as SolverIcingSession
from ansys.fluent.core.session.solver_lite import SolverLite as SolverLiteSession
from ansys.fluent.core.session.solver_pre_post import PrePost

__all__ = [
    "MeshingSession",
    "PureMeshingSession",
    "SolverSession",
    "SolverAeroSession",
    "SolverIcingSession",
    "SolverLiteSession",
    "FileSession",
    "PrePost",
]
