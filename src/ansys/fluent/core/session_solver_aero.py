"""Module containing class encapsulating Fluent connection.

Expose aero capabilities.
"""

from typing import Any, Dict

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.session_solver import Solver


class SolverAero(Solver):
    """Encapsulates a Fluent server for Aero session connection.

    SolverAero(Session) holds the top-level objects for solver TUI, settings and aero
    datamodel objects calls.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """SolverAero session.

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
        super(SolverAero, self).__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
        )
        self._flserver_root = None
        self._fluent_version = None
        self._fluent_connection = fluent_connection
        # TODO: Update Aero DM
        scheme_eval.scheme_eval("(aero-load-addon)")

    def new_project(self, project_name: str):
        """Define a new project."""
        # TODO: Update Aero DM
        self.scheme_eval.scheme_eval(f"""(prjapp-new-project-cb #f "{project_name}")""")

    def open_project(self, project_name: str):
        """Open a saved project."""
        # TODO: Update Aero DM
        self.scheme_eval.scheme_eval(
            f"""(prjapp-project-open-project-cb #f "{project_name}")"""
        )

    def new_simulation(self, case_file_name: str):
        """Add a new simulation by loading a case-file."""
        # TODO: Update Aero DM
        self.scheme_eval.scheme_eval(
            f"""(gui-aero-project-add-workflow-cb #f "{case_file_name}" #f #f)"""
        )

    def open_simulation(self, simulation_file_name: str):
        """Open a saved simulation."""
        # TODO: Update Aero DM
        self.scheme_eval.scheme_eval(
            f"""(aero-server-project-open-simulation "{simulation_file_name}")"""
        )

    @property
    def _flserver(self):
        """Root datamodel object."""
        return PyMenuGeneric(service=self._se_service, rules="flserver")

    @property
    def aero(self):
        """Instance of aero (Case.App) -> root datamodel object."""
        return self._flserver.Case.App

    def __dir__(self):
        return super(SolverAero, self).__dir__()
