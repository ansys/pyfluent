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

The session classes are organized by responsibility:

* :class:`BaseSession` and :class:`FileSession` are defined in
    :mod:`ansys.fluent.core.execution.session.session` and
    :mod:`ansys.fluent.core.execution.session.file`, respectively.
* Solver sessions are defined in modules under
    :mod:`ansys.fluent.core.solver.session`.
* Meshing sessions are defined in modules under
    :mod:`ansys.fluent.core.meshing.session`.

The refactor moved the session implementations into these execution, solver,
and meshing packages; their inheritance relationships are unchanged. The
public hierarchy is::

        BaseSession (execution.session.session)
        ├── Solver (solver.session.solver)
        │   ├── SolverAero (solver.session.solver_aero)
        │   ├── SolverIcing (solver.session.solver_icing)
        │   ├── SolverLite (solver.session.solver_lite)
        │   └── PrePost (solver.session.solver_pre_post)
        └── BaseMeshing (meshing.session.base_meshing; internal base class)
                ├── PureMeshing (meshing.session.pure_meshing)
                └── Meshing (meshing.session.meshing)

:class:`~ansys.fluent.core.execution.session.file.FileSession` is a separate file-based reader, not a live Fluent session and
not a subclass of :class:`~ansys.fluent.core.execution.session.session.BaseSession`. It is defined in
:mod:`ansys.fluent.core.execution.session.file`.

This package re-exports the concrete solver, meshing, and file-session classes
for convenience. Their defining modules are listed above; :class:`~ansys.fluent.core.execution.session.session.BaseSession` is
available from :mod:`ansys.fluent.core.execution.session.session`.
"""


from ansys.fluent.core.execution.session.file import FileSession
from ansys.fluent.core.meshing.session.meshing import Meshing
from ansys.fluent.core.meshing.session.pure_meshing import PureMeshing
from ansys.fluent.core.solver.session.solver import Solver
from ansys.fluent.core.solver.session.solver_aero import SolverAero
from ansys.fluent.core.solver.session.solver_icing import SolverIcing
from ansys.fluent.core.solver.session.solver_lite import SolverLite
from ansys.fluent.core.solver.session.solver_pre_post import PrePost

__all__ = [
    "Meshing",
    "PureMeshing",
    "Solver",
    "SolverAero",
    "SolverIcing",
    "SolverLite",
    "FileSession",
    "PrePost",
]
