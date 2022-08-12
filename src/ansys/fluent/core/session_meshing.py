"""Module containing class encapsulating Fluent connection."""
# import weakref


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

    def switch_to_solver(self):
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(fluent_connection=self.fluent_connection)
        # self._alive.remove(self)
        return solver_session
