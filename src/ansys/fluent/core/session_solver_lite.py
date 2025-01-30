# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""

from typing import Any, Dict

from ansys.fluent.core.session_solver import Solver


class SolverLite(Solver):
    """Encapsulates a Fluent - Solver(Lite) session connection.
    SolverLite(Session) holds the top-level objects
    for solver TUI and settings objects calls."""

    def __init__(
        self,
        fluent_connection=None,
        scheme_eval=None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """SolverLite session.

        Parameters
        ----------
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
            scheme_eval: SchemeEval
                Instance of ``SchemeEval`` to execute Fluent's scheme code on.
            start_transcript : bool, optional
                Whether to start the Fluent transcript in the client.
                The default is ``True``, in which case the Fluent transcript can be subsequently
                started and stopped using method calls on the ``Session`` object.
        """
        super().__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
        )
        self._tui_service = self._datamodel_service_tui
        self._settings_service = self.settings_service
        self._tui = None
        self._settings_root = None

    # One can inherit methods from 'Solver' and re-define it here to make it unavailable in solver-Lite

    def switch_to_full_solver(self):
        """A switch to move to the full-solver session from solver-lite."""
        solver_session = Solver(
            fluent_connection=self._fluent_connection, scheme_eval=self.scheme_eval
        )
        return solver_session
