"""Module containing class encapsulating Fluent connection."""

from typing import Any, Optional

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver


class Meshing(PureMeshing):
    """Encapsulates a Fluent meshing session.

    A ``tui`` object
    for meshing TUI commanding, and ``meshing`` and ``workflow``
    objects for access to task-based meshing workflows are all
    exposed here. A ``switch_to_solver`` method is available
    in this mode.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        file_transfer_service: Optional[Any] = None,
    ):
        """Meshing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
            file_transfer_service: Supports file upload and download.
        """
        super(Meshing, self).__init__(
            fluent_connection=fluent_connection,
            file_transfer_service=file_transfer_service,
        )
        self.switch_to_solver = lambda: self._switch_to_solver()
        self.switched = False

    def _switch_to_solver(self) -> Any:
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(
            fluent_connection=self._fluent_connection,
            file_transfer_service=self._file_transfer_service,
        )
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
        """Datamodel root of meshing."""
        return super(Meshing, self).meshing if not self.switched else None

    @property
    def meshing_utilities(self):
        """Datamodel root of meshing_utilities."""
        return super(Meshing, self).meshing_utilities if not self.switched else None

    @property
    def workflow(self):
        """Datamodel root of workflow."""
        return super(Meshing, self).workflow if not self.switched else None

    @property
    def PartManagement(self):
        """Datamodel root of PartManagement."""
        return super(Meshing, self).PartManagement if not self.switched else None

    @property
    def PMFileManagement(self):
        """Datamodel root of PMFileManagement."""
        return super(Meshing, self).PMFileManagement if not self.switched else None

    @property
    def preferences(self):
        """Datamodel root of preferences."""
        return super(Meshing, self).preferences if not self.switched else None
