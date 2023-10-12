"""Module containing class encapsulating Fluent connection."""
import os
import time
from typing import Any

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
import ansys.platform.instancemanagement as pypim


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
    ):
        """Meshing session.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
        """
        super(Meshing, self).__init__(fluent_connection=fluent_connection)
        self._fluent_connection = fluent_connection
        self.switch_to_solver = lambda: self._switch_to_solver()
        self.switched = False
        self._server_file_manager = None

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
        """Datamodel root of meshing."""
        return super(Meshing, self).meshing if not self.switched else None

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
