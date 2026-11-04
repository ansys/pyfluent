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

"""Solver session classes for full, add-on, and specialized Fluent workflows.

The :class:`Solver` session provides the standard Fluent solver API and
inherits from :class:`~ansys.fluent.core.execution.session.session.BaseSession`.
The :class:`SolverAero`, :class:`SolverIcing`, :class:`SolverLite`, and
:class:`PrePost` session classes specialize ``Solver`` for their respective
workflows. These concrete session classes are re-exported by
:mod:`ansys.fluent.core.execution.session` and the top-level
``ansys.fluent.core`` package.
"""

from ansys.fluent.core.solver.session.solver import Solver
from ansys.fluent.core.solver.session.solver_aero import SolverAero
from ansys.fluent.core.solver.session.solver_icing import SolverIcing
from ansys.fluent.core.solver.session.solver_lite import SolverLite
from ansys.fluent.core.solver.session.solver_pre_post import PrePost

__all__ = ("Solver", "SolverAero", "SolverIcing", "SolverLite", "PrePost")
