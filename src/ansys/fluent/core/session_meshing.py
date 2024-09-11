"""Module containing class encapsulating Fluent connection."""

from typing import Any, Dict

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
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
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """Meshing session.

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
        self.switched = False
        super(Meshing, self).__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
        )

    def switch_to_solver(self) -> Any:
        """Switch to solver mode and return a solver session object. Deactivate this
        object's public interface and streaming services.

        Returns
        -------
        Solver
        """
        for cb in self._fluent_connection.finalizer_cbs:
            cb()
        self.tui.switch_to_solution_mode("yes")
        solver_session = Solver(
            fluent_connection=self._fluent_connection,
            scheme_eval=self.scheme_eval,
            file_transfer_service=self._file_transfer_service,
        )
        self.switched = True
        return solver_session

    def __getattribute__(self, item: str):
        if item == "switched":
            return super(Meshing, self).__getattribute__(item)

        if self.switched and item != "exit":
            return None

        return super(Meshing, self).__getattribute__(item)

    @property
    def tui(self):
        """Meshing TUI root."""
        return super(Meshing, self).tui

    @property
    def meshing(self):
        """Meshing datamodel root."""
        return super(Meshing, self).meshing

    @property
    def meshing_utilities(self):
        """Meshing utilities datamodel root."""
        return super(Meshing, self).meshing_utilities

    @property
    def workflow(self):
        """Workflow datamodel root."""
        return super(Meshing, self).workflow

    @property
    def PartManagement(self):
        """Part management datamodel root."""
        return super(Meshing, self).PartManagement

    @property
    def PMFileManagement(self):
        """Part management file management datamodel root."""
        return super(Meshing, self).PMFileManagement

    @property
    def preferences(self):
        """Preferences datamodel root."""
        return super(Meshing, self).preferences
