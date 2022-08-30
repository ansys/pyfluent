"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""
import importlib

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath


class SolverIcing(Solver):
    """Encapsulates a Fluent server for Icing session connection.

    SolverIcing(Session) holds the top-level objects for solver TUI,
    settings and icing datamodel objects calls.
    """

    def __init__(
        self,
        fluent_connection: _FluentConnection,
    ):
        super(SolverIcing, self).__init__(fluent_connection=fluent_connection)
        self._flserver_root = None
        self._version = None
        self._fluent_connection = fluent_connection

    def get_fluent_version(self):
        """Gets and returns the fluent version."""
        return self._fluent_connection.get_fluent_version()

    @property
    def version(self):
        if self._version is None:
            self._version = get_version_for_filepath(session=self)
        return self._version

    @property
    def _flserver(self):
        """root datamodel object."""
        if self._flserver_root is None:
            se = self.fluent_connection.datamodel_service_se
            dm_module = tui_module = importlib.import_module(
                f"ansys.fluent.core.datamodel_{self.version}.flicing"
            )
            self._flserver_root = dm_module.Root(se, "flserver", [])
        return self._flserver_root

    @property
    def icing(self):
        """instance of icing (Case.App) -> root datamodel object."""
        return self._flserver.Case.App
