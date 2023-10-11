"""Module containing class encapsulating Fluent connection."""
import os
from pathlib import Path
import time
from typing import Any, Optional

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.utils.client import Client


class Meshing(PureMeshing):
    """Encapsulates a Fluent meshing session. A ``tui`` object
    for meshing TUI commanding, and ``meshing`` and ``workflow``
    objects for access to task-based meshing workflows are all
    exposed here. A ``switch_to_solver`` method is available
    in this mode."""

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
        file_name,
        upload_file_path: Optional[str] = None,
    ):
        """Reads and uploads a file.

        Parameters
        ----------
        file_name : str
            Case file name
        upload_file_path : str, optional, default None
            Case file path to upload a case file
        """
        if not self._server_file_manager:
            self._server_file_manager = _ServerFileManager(self._fluent_connection)
        return self._server_file_manager.read_case(
            file_name,
            upload_file_path,
        )

    def write_case(
        self,
        file_name: str,
        download_file_path: Optional[str] = None,
    ):
        """Writes and downloads a file.

        Parameters
        ----------
        file_name : str
            Case file name
        download_file_path : str, optional, default False
            File path to download a case file
        """
        if not self._server_file_manager:
            self._server_file_manager = _ServerFileManager(self._fluent_connection)
        return self._server_file_manager.write_case(file_name, download_file_path)


class _ServerFileManager(Meshing):
    """Supports file upload and download for every existing file read,
    write methods respectively in the cloud particularly in Ansys lab.
    Here we are supporting upload and download methods in existing session
    methods. These would be no-ops if PyPIM is not configured or not authorized
    with the appropriate service. This will be used for internal purpose only.

    Methods
    -------
    read_case(
        file_name, upload_file_path, remote_file_name
        )
        Read and upload a case file.

    write_case(
        file_name, upload_file_path, remote_file_name
        )
        Write and download a case file.
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
            self.file_service = Client(
                token="token", url=upload_server.uri, headers=upload_server.headers
            )

    def read_case(
        self,
        file_name,
        upload_file_path: Optional[str] = None,
    ):
        """Reads and uploads a file.

        Parameters
        ----------
        file_name : str
            Case file name
        upload_file_path : str, optional, default None
            Case file path to upload a case file
        """
        if upload_file_path:
            if os.path.isfile(upload_file_path):
                print("\nUploading file on the server...\n")
            else:
                raise FileNotFoundError(f"{upload_file_path} does not exist.")
            self.upload(upload_file_path)
            time.sleep(5)
            print("\nFile is uploaded.\n")
            if self.file_service.file_exist(file_name):
                self.tui.file.read_case(file_name)
            else:
                raise FileNotFoundError("\nFile does not exist.\n")
        else:
            self.tui.file.read_case(file_name)

    def write_case(
        self,
        file_name: str,
        download_file_path: Optional[str] = None,
    ):
        """Writes and downloads a file.

        Parameters
        ----------
        file_name : str
            Case file name
        download_file_path : str, optional, default False
            File path to download a case file
        """
        self.tui.file.write_case(file_name)
        time.sleep(5)
        if download_file_path:
            print("\nChecking if specified file already exists...\n")
            file_path = Path(download_file_path) / file_name
            if os.path.isfile(file_path):
                print(f"\nFile already exists. File path:\n{file_path}\n")
            else:
                print("\nFile does not exist. Downloading specified file...\n")
                if self.file_service.file_exist(file_name):
                    if not os.path.exists(download_file_path):
                        os.makedirs(download_file_path)
                    self.download(file_name, download_file_path)
                else:
                    raise FileNotFoundError("\nFile does not exist on the server.\n")
                print("File is downloaded.")
