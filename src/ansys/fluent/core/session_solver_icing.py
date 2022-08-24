"""Module containing class encapsulating Fluent connection.

**********PRESENTLY SAME AS SOLVER WITH A SWITCH TO SOLVER***********
"""
from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session_solver import Solver


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

    @property
    def _flserver(self):
        """root datamodel object."""
        if self._flserver_root is None:
            from ansys.fluent.core.datamodel.flicing import Root as icing_root

            se = self.fluent_connection.datamodel_service_se
            self._flserver_root = icing_root(se, "flserver", [])
        return self._flserver_root

    @property
    def icing(self):
        """instance of icing (Case.App) -> root datamodel object."""
        return self._flserver.Case.App
