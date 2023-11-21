"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""
import importlib
from typing import Any, Optional

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session_solver import Solver


class SolverIcing(Solver):
    """Encapsulates a Fluent server for Icing session connection.

    SolverIcing(Session) holds the top-level objects for solver TUI, settings and icing
    datamodel objects calls.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        remote_file_handler: Optional[Any] = None,
    ):
        """SolverIcing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
            remote_file_handler: Supports file upload and download.
        """
        super(SolverIcing, self).__init__(
            fluent_connection=fluent_connection, remote_file_handler=remote_file_handler
        )
        self._flserver_root = None
        self._version = None
        self._fluent_connection = fluent_connection

    @property
    def _flserver(self):
        """Root datamodel object."""
        if self._flserver_root is None:
            se = self.datamodel_service_se
            dm_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self.version}.flicing"
            )
            self._flserver_root = dm_module.Root(se, "flserver", [])
        return self._flserver_root

    @property
    def icing(self):
        """Instance of icing (Case.App) -> root datamodel object."""
        return self._flserver.Case.App
