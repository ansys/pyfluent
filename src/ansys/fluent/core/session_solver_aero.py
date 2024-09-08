"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""

from typing import Any, Dict, Optional

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.session_solver import Solver


class SolverAero(Solver):
    """Encapsulates a Fluent server for Aero session connection.

    SolverAero(Session) holds the top-level objects for solver TUI, settings and aero
    datamodel objects calls.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Optional[Any] = None,
        start_transcript: bool = True,
        launcher_args: Optional[Dict[str, Any]] = None,
    ):
        """SolverAero session.

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
        super(SolverAero, self).__init__(
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
        return PyMenuGeneric(service=self._se_service, rules="flserver")

    @property
    def aero(self):
        """Instance of aero (Case.App) -> root datamodel object."""
        return self._flserver.Case.App

    def __dir__(self):
        return super(SolverAero, self).__dir__()
