"""Module containing class encapsulating Fluent connection."""

import functools
from typing import Any, Optional

import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services.meshing_queries import (
    MeshingQueries,
    MeshingQueriesService,
)
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
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

    def __init__(
        self,
        fluent_connection: FluentConnection,
        file_transfer_service: Optional[Any] = None,
    ):
        """PureMeshing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
            file_transfer_service: Supports file upload and download.
        """
        super(PureMeshing, self).__init__(
            fluent_connection=fluent_connection,
            file_transfer_service=file_transfer_service,
        )
        self._base_meshing = BaseMeshing(
            self.execute_tui,
            fluent_connection,
            self.get_fluent_version().value,
            self.datamodel_service_tui,
            self.datamodel_service_se,
        )

        self.meshing_queries_service = fluent_connection.create_grpc_service(
            MeshingQueriesService, self._error_state
        )

        datamodel_service_se = self.datamodel_service_se
        self.datamodel_streams = {}
        if pyfluent.DATAMODEL_USE_STATE_CACHE:
            for _rules in rules:
                stream = DatamodelStream(datamodel_service_se)
                stream.register_callback(
                    functools.partial(DataModelCache.update_cache, rules=_rules)
                )
                self.datamodel_streams[_rules] = stream
                stream.start(
                    rules=_rules,
                    no_commands_diff_state=pyfluent.DATAMODEL_USE_NOCOMMANDS_DIFF_STATE,
                )
                self.fluent_connection.register_finalizer_cb(stream.stop)

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
    def meshing_queries(self):
        """Datamodel root of meshing_queries."""
        if self.get_fluent_version() >= FluentVersion.v232:
            return MeshingQueries(self.meshing_queries_service)

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
        self._base_meshing.watertight_workflow.reinitialize()
        return self._base_meshing.watertight_workflow

    def fault_tolerant(self):
        """Get a new fault-tolerant workflow."""
        self._base_meshing.fault_tolerant_workflow.reinitialize()
        return self._base_meshing.fault_tolerant_workflow

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
        file_name_stem: Optional[str] = None,
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


rules = [
    "workflow",
    "meshing",
    "MeshingUtilities",
    "PartManagement",
    "PMFileManagement",
]

for r in rules:
    DataModelCache.set_config(r, "name_key", NameKey.INTERNAL)
