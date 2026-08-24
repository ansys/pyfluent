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

"""Fluent meshing session with solver-switching capability (:class:`Meshing`).

Inheritance
-----------
::

    BaseSession (private)
    └── BaseMeshing (private)
        └── Meshing          ← this class
"""

from typing import TYPE_CHECKING, Any

from ansys.fluent.core.session.base_meshing import BaseMeshing
from ansys.fluent.core.session.session import BaseSession
from ansys.fluent.core.session.solver import Solver


class Meshing(BaseMeshing):
    """Fluent meshing session with the ability to switch to a solver.

    Extends :class:`~ansys.fluent.core.session.base_meshing.BaseMeshing` by
    adding :meth:`switch_to_solver`, which transitions the running Fluent
    process from meshing mode to solver mode and returns a
    :class:`~ansys.fluent.core.session.solver.Solver` instance.

    All attributes and workflow factory methods of
    :class:`~ansys.fluent.core.session.base_meshing.BaseMeshing` are available
    here.  After :meth:`switch_to_solver` is called this object is deactivated
    and must not be used.
    """

    def switch_to_solver(self) -> Any:
        """Switch to solver mode and return a solver session object. Deactivate this
        object's public interface and streaming services.

        Returns
        -------
        Solver
        """
        for cb in self._fluent_connection.finalizer_cbs:
            cb()
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(
            fluent_connection=self._fluent_connection,
            scheme_eval=self.scheme,
            file_transfer_service=self._file_transfer_service,
        )
        self._fluent_connection = None
        self.__doc__ = (
            "The meshing session is no longer usable after switching to solution mode."
        )
        return solver_session

    if not TYPE_CHECKING:

        def __getattribute__(self, item: str):
            if item.startswith("__") and item.endswith("__"):
                return super().__getattribute__(item)
            try:
                _connection = super().__getattribute__("_fluent_connection")
            except AttributeError:
                _connection = False
            if (
                _connection is None
                and item not in BaseSession._inactive_session_allow_list
            ):
                raise AttributeError(
                    f"'{type(self).__name__}' object has no attribute '{item}'"
                )

            return super().__getattribute__(item)
