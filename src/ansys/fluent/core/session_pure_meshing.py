"""Module containing class encapsulating Fluent connection."""

import functools
import os
import time
from typing import Optional

import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.services.meshing_queries import (
    MeshingQueries,
    MeshingQueriesService,
)
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_base_meshing import BaseMeshing
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.utils.data_transfer import transfer_case
import ansys.platform.instancemanagement as pypim


class PureMeshing(BaseSession):
    """Encapsulates a Fluent meshing session.

    A ``tui`` object
    for meshing TUI commanding, and ``meshing`` and ``workflow``
    objects for access to task-based meshing workflows are all
    exposed here. No ``switch_to_solver`` method is available
    in this mode.
    """

    rules = ["workflow", "meshing", "PartManagement", "PMFileManagement"]
    for r in rules:
        DataModelCache.set_config(r, "internal_names_as_keys", True)

    def __init__(self, fluent_connection: FluentConnection):
        """PureMeshing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
        """
        super(PureMeshing, self).__init__(fluent_connection=fluent_connection)
        self._fluent_connection = fluent_connection
        self._server_file_manager = None
        self._base_meshing = BaseMeshing(
            self.execute_tui,
            fluent_connection,
            self.get_fluent_version(),
            self.datamodel_service_tui,
            self.datamodel_service_se,
        )

        self.meshing_queries_service = fluent_connection.create_service(
            MeshingQueriesService, self.error_state
        )
        self.meshing_queries = MeshingQueries(self.meshing_queries_service)

        datamodel_service_se = self.datamodel_service_se
        self.datamodel_streams = {}
        if pyfluent.DATAMODEL_USE_STATE_CACHE:
            for rules in self.__class__.rules:
                stream = DatamodelStream(datamodel_service_se)
                stream.register_callback(
                    functools.partial(DataModelCache.update_cache, rules=rules)
                )
                self.datamodel_streams[rules] = stream
                stream.start(
                    rules=rules,
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
    def workflow(self):
        """Datamodel root of workflow."""
        return self._base_meshing.workflow

    def watertight(self, dynamic_interface=True):
        """Get a new watertight workflow."""
        self.workflow.watertight(dynamic_interface)
        return self.workflow

    def fault_tolerant(self, dynamic_interface=True):
        """Get a new fault-tolerant workflow."""
        self.workflow.fault_tolerant(dynamic_interface)
        return self.workflow

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

    def read_case(
        self,
        file_name: str,
    ):
        """Reads a case file.

        Parameters
        ----------
        file_name : str
            Case file name
        """
        if not self._server_file_manager:
            self._server_file_manager = _ServerFileManager(self._fluent_connection)
        return self._server_file_manager.read_case(
            file_name,
        )

    def write_case(
        self,
        file_name: str,
    ):
        """Writes a case file.

        Parameters
        ----------
        file_name : str
            Case file name
        """
        if not self._server_file_manager:
            self._server_file_manager = _ServerFileManager(self._fluent_connection)
        return self._server_file_manager.write_case(file_name)


class _ServerFileManager(Meshing):
    """Supports file upload and download for every existing file read,
    write methods respectively in the cloud particularly in Ansys lab.
    Here we are supporting upload and download methods in existing session
    methods. These would be no-ops if PyPIM is not configured or not authorized
    with the appropriate service. This will be used for internal purpose only.

    Methods
    -------
    read_case(
        file_name
        )
        Read a case file.

    write_case(
        file_name
        )
        Write a case file.
    """

    def __init__(self, fluent_connection):
        super(_ServerFileManager, self).__init__(fluent_connection)
        self.pim_instance = fluent_connection._remote_instance
        self.file_service = None
        try:
            upload_server = self.pim_instance.services["http-simple-upload-server"]
        except (AttributeError, KeyError):
            pass
        else:
            from simple_upload_server.client import Client

            self.file_service = Client(
                token="token", url=upload_server.uri, headers=upload_server.headers
            )

    def _wait_for_file(self, file_name, file_service):
        start_time = time.time()
        max_wait_time = 100
        while (time.time() - start_time) < max_wait_time:
            if file_service.file_exist(os.path.basename(file_name)):
                break
            max_wait_time -= 1
            time.sleep(3)
        else:
            raise FileNotFoundError(f"{file_name} does not exist.")

    def read_case(
        self,
        file_name: str,
    ):
        """Reads  a case file.

        Parameters
        ----------
        file_name : str
            Case file name

        Raises
        ------
        FileNotFoundError
            If a case file does not exist.
        """
        if pypim.is_configured():
            if os.path.isfile(file_name):
                if not self.file_service.file_exist(os.path.basename(file_name)):
                    self.upload(os.path.basename(file_name))
                    self._wait_for_file(file_name, self.file_service)
            elif self.file_service.file_exist(os.path.basename(file_name)):
                pass
            else:
                raise FileNotFoundError(f"{file_name} does not exist.")
            self.tui.file.read_case(os.path.basename(file_name))
        else:
            self.tui.file.read_case(file_name)

    def write_case(
        self,
        file_name: str,
    ):
        """Writes a case file.

        Parameters
        ----------
        file_name : str
            Case file name
        """
        self.tui.file.write_case(os.path.basename(file_name))
        if pypim.is_configured():
            self._wait_for_file(file_name, self.file_service)
            if os.path.isfile(file_name):
                print(f"\nFile already exists. File path:\n{file_name}\n")
            else:
                self.download(os.path.basename(file_name), ".")
