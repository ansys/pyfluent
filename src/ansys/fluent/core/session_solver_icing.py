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

Expose icing capabilities.
"""

import importlib
from typing import Any, Dict

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
from ansys.fluent.core.session_solver import Solver


class SolverIcing(Solver):
    """Encapsulates a Fluent server for Icing session connection.

    SolverIcing(Session) holds the top-level objects for solver TUI, settings and icing
    datamodel objects calls.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """SolverIcing session.

        Parameters
        ----------
        fluent_connection (:ref:`ref_fluent_connection`):
            Encapsulates a Fluent connection.
        scheme_eval: SchemeEval
            Instance of ``SchemeEval`` to execute Fluent's scheme code on.
        file_transfer_service : Optional
            Service for uploading and downloading files.
        start_transcript : bool, optional
            Whether to start the Fluent transcript in the client.
            The default is ``True``, in which case the Fluent
            transcript can be subsequently started and stopped
            using method calls on the ``Session`` object.
        """
        super(SolverIcing, self).__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
        )
        self._flserver_root = None
        self._fluent_version = None
        self._fluent_connection = fluent_connection

    @property
    def _flserver(self):
        """Root datamodel object."""
        if self._flserver_root is None:
            se = self._datamodel_service_se
            dm_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self._version}.flicing"
            )
            self._flserver_root = dm_module.Root(se, "flserver", [])
        return self._flserver_root

    @property
    def icing(self):
        """Instance of icing (Case.App) -> root datamodel object."""
        return self._flserver.Case.App

    def __dir__(self):
        return super(SolverIcing, self).__dir__()
