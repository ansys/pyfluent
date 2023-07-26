"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""
import importlib

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath


class SolverIcing(Solver):
    """Encapsulates a Fluent server for Icing session connection.

    SolverIcing(Session) holds the top-level objects for solver TUI,
    settings and icing datamodel objects calls.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
    ):
        """SolverIcing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
        """
        super(SolverIcing, self).__init__(fluent_connection=fluent_connection)
        self._flserver_root = None
        self._version = None
        self._fluent_connection = fluent_connection

    @property
    def version(self):
        """Fluent's product version."""
        if self._version is None:
            self._version = get_version_for_filepath(session=self)
        return self._version

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
