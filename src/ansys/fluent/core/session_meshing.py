"""Module containing class encapsulating Fluent connection."""

from typing import Any

from ansys.fluent.core.fluent_connection import _FluentConnection
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
        self.switched = False

    def _switch_to_solver(self) -> Any:
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(fluent_connection=self.fluent_connection)
        delattr(self, "switch_to_solver")
        self.switched = True
        return solver_session

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        return super(Meshing, self).tui if not self.switched else None

    @property
    def meshing(self):
        """meshing datamodel root."""
        return super(Meshing, self).meshing if not self.switched else None

    @property
    def workflow(self):
        """workflow datamodel root."""
        return super(Meshing, self).workflow if not self.switched else None

    @property
    def PartManagement(self):
        """PartManagement datamodel root."""
        return super(Meshing, self).PartManagement if not self.switched else None

    @property
    def PMFileManagement(self):
        """PMFileManagement datamodel root."""
        return super(Meshing, self).PMFileManagement if not self.switched else None

    @property
    def preferences(self):
        """preferences datamodel root."""
        return super(Meshing, self).preferences if not self.switched else None
