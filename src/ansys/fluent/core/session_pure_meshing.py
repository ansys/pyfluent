"""Module containing class encapsulating Fluent connection.
"""


import functools

from ansys.api.fluent.v0 import datamodel_se_pb2
import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services.streaming import StreamingService
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.utils.data_transfer import transfer_case


class PureMeshing(BaseSession):
    """Encapsulates a Fluent meshing session. A ``tui`` object
    for meshing TUI commanding, and ``meshing`` and ``workflow``
    objects for access to task-based meshing workflows are all
    exposed here. No ``switch_to_solver`` method is available
    in this mode."""

    rules = ["workflow", "meshing", "PartManagement", "PMFileManagement"]
    for r in rules:
        DataModelCache.set_config(r, "internal_names_as_keys", True)

    def __init__(self, fluent_connection: FluentConnection):
        """PureMeshing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
        """
        super(PureMeshing, self).__init__(fluent_connection=fluent_connection)
        self._base_meshing = BaseMeshing(self.execute_tui, fluent_connection)
        datamodel_service_se = fluent_connection.datamodel_service_se
        self.datamodel_streams = {}
        if pyfluent.DATAMODEL_USE_STATE_CACHE:
            for rules in self.__class__.rules:
                request = datamodel_se_pb2.DataModelRequest()
                request.rules = rules
                if pyfluent.DATAMODEL_USE_NOCOMMANDS_DIFF_STATE:
                    request.diffstate = datamodel_se_pb2.DIFFSTATE_NOCOMMANDS
                streaming = StreamingService(
                    stub=datamodel_service_se._stub,
                    request=request,
                    metadata=datamodel_service_se._metadata,
                )
                stream = DatamodelStream(streaming)
                stream.register_callback(
                    functools.partial(DataModelCache.update_cache, rules=rules)
                )
                self.datamodel_streams[rules] = stream
                stream.start()

    @property
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        return self._base_meshing.tui

    @property
    def meshing(self):
        """meshing datamodel root."""
        return self._base_meshing.meshing

    @property
    def workflow(self):
        """workflow datamodel root."""
        return self._base_meshing.workflow

    @property
    def PartManagement(self):
        """PartManagement datamodel root."""
        return self._base_meshing.PartManagement

    @property
    def PMFileManagement(self):
        """PMFileManagement datamodel root."""
        return self._base_meshing.PMFileManagement

    @property
    def preferences(self):
        """preferences datamodel root."""
        return self._base_meshing.preferences

    def transfer_mesh_to_solvers(
        self,
        solvers,
        file_type: str = "case",
        file_name_stem: str = None,
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
