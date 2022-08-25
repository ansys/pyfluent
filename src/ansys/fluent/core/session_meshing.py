"""Module containing class encapsulating Fluent connection."""

from typing import Any

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session_base_meshing import _BaseMeshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver


class Meshing(PureMeshing):
    """Encapsulates a Fluent - Meshing session connection.
    Meshing(PureMeshing) holds the top-level objects
    for meshing TUI and various meshing datamodel API calls.
    In this general meshing mode, switch to solver is available,
    after which"""

    def __init__(
        self,
        fluent_connection: _FluentConnection,
    ):
        super(Meshing, self).__init__(fluent_connection=fluent_connection)
        self.switch_to_solver = lambda: self._switch_to_solver()

    def _switch_to_solver(self) -> Any:
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(fluent_connection=self.fluent_connection)
        for attr in _BaseMeshing.meshing_attrs + ("switch_to_solver",):
            delattr(self, attr)
        return solver_session
