"""Module containing class encapsulating Fluent connection."""
# import weakref


from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver


class Meshing(PureMeshing):
    """Encapsulates a Fluent - Meshing session connection.
    Meshing(PureMeshing) holds the top-level objects
    for meshing TUI and various meshing datamodel API calls."""

    """
    _alive = []

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        Meshing._alive.append(self)
        return weakref.proxy(self)
    """

    def __init__(
        self,
        fluent_connection: _FluentConnection,
    ):
        super(Meshing, self).__init__(fluent_connection=fluent_connection)

    def switch_to_solver(self):
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(fluent_connection=self.fluent_connection)
        # self._alive.remove(self)
        return solver_session
