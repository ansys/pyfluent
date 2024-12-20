"""Module containing class encapsulating Fluent connection."""

import functools
from typing import Any, Dict

import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services import SchemeEval
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.streaming_services.events_streaming import MeshingEvent
from ansys.fluent.core.utils.data_transfer import transfer_case
from ansys.fluent.core.utils.fluent_version import FluentVersion


class PureMeshing(BaseSession):
    """Encapsulates a Fluent meshing session.

    A ``tui`` object
    for meshing TUI commanding, and ``meshing`` and ``workflow``
    objects for access to task-based meshing workflows are all
    exposed here. No ``switch_to_solver`` method is available
    in this mode.
    """

    _rules = [
        "workflow",
        "meshing",
        "MeshingUtilities",
        "PartManagement",
        "PMFileManagement",
    ]

    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """PureMeshing session.

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
        super(PureMeshing, self).__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
            event_type=MeshingEvent,
        )
        self._base_meshing = BaseMeshing(
            self.execute_tui,
            fluent_connection,
            self.get_fluent_version().value,
            self._datamodel_service_tui,
            self._datamodel_service_se,
        )

        datamodel_service_se = self._datamodel_service_se
        self.datamodel_streams = {}
        if datamodel_service_se.cache is not None:
            for rules in PureMeshing._rules:
                datamodel_service_se.cache.set_config(
                    rules,
                    "name_key",
                    (
                        NameKey.DISPLAY
                        if DataModelCache.use_display_name
                        else NameKey.INTERNAL
                    ),
                )
                stream = DatamodelStream(datamodel_service_se)
                stream.register_callback(
                    functools.partial(
                        datamodel_service_se.cache.update_cache,
                        rules=rules,
                        version=datamodel_service_se.version,
                    )
                )
                self.datamodel_streams[rules] = stream
                stream.start(
                    rules=rules,
                    no_commands_diff_state=pyfluent.DATAMODEL_USE_NOCOMMANDS_DIFF_STATE,
                )
                self._fluent_connection.register_finalizer_cb(stream.stop)

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        return self._base_meshing.tui

    @property
    def meshing(self):
        """Datamodel root of meshing."""
        return self._base_meshing.meshing

    @property
    def meshing_utilities(self):
        """Datamodel root of meshing_utilities."""
        if self.get_fluent_version() >= FluentVersion.v242:
            return self._base_meshing.meshing_utilities

    @property
    def workflow(self):
        """Datamodel root of workflow."""
        return self._base_meshing.workflow

    def watertight(self):
        """Get a new watertight workflow."""
        return self._base_meshing.watertight_workflow()

    def fault_tolerant(self):
        """Get a new fault-tolerant workflow."""
        return self._base_meshing.fault_tolerant_workflow()

    def two_dimensional_meshing(self):
        """Get a new 2D meshing workflow."""
        return self._base_meshing.two_dimensional_meshing_workflow()

    def load_workflow(self, file_path: str):
        """Load a saved workflow."""
        return self._base_meshing.load_workflow(file_path=file_path)

    def create_workflow(self):
        """Create a meshing workflow."""
        return self._base_meshing.create_workflow()

    @property
    def current_workflow(self):
        """Current meshing workflow."""
        return self._base_meshing.current_workflow

    def topology_based(self):
        """Get a new topology-based meshing workflow.

        Raises
        ------
        RuntimeError
            If beta features are not enabled in Fluent.
        """
        if not self._app_utilities.is_beta_enabled():
            raise RuntimeError("Topology-based Meshing is a beta feature in Fluent.")
        self._base_meshing.topology_based_meshing_workflow.initialize()
        return self._base_meshing.topology_based_meshing_workflow

    @property
    def PartManagement(self):
        """Datamodel root of PartManagement."""
        return self._base_meshing.PartManagement

    @property
    def PMFileManagement(self):
        """Datamodel root of PMFileManagement."""
        return self._base_meshing.PMFileManagement

    @property
    def preferences(self):
        """Datamodel root of preferences."""
        return self._base_meshing.preferences

    def transfer_mesh_to_solvers(
        self,
        solvers,
        file_type: str = "case",
        file_name_stem: str | None = None,
        num_files_to_try: int = 1,
        clean_up_mesh_file: bool = True,
        overwrite_previous: bool = True,
    ):
        """Transfer mesh to Fluent solver instances.

        Parameters
        ----------
        solvers : iterable
            Sequence of solver instances
        file_type : str, default "case"
            "case" or "mesh"
        file_name_stem : str
            Optional file name stem
        num_files_to_try : int, default 1
            Optional number of files to try to write,
            each with a different generated name.
            Defaults to 1
        clean_up_mesh_file: bool, default True
            Whether to remove the file at the end
        overwrite_previous: bool, default True
            Whether to overwrite the file if it already exists
        Returns
        -------
        None
        """
        transfer_case(
            self,
            solvers,
            file_type,
            file_name_stem,
            num_files_to_try,
            clean_up_mesh_file,
            overwrite_previous,
        )
