"""Provides a module for file transfer service."""

import os
import pathlib
import shutil
import subprocess
from typing import Any, Callable, Optional, Protocol, Union  # noqa: F401

from alive_progress import alive_bar
import platformdirs

from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
import ansys.platform.instancemanagement as pypim
import ansys.tools.filetransfer as ft


class PyPIMConfigurationError(ConnectionError):
    """Raised when `PyPIM<https://pypim.docs.pyansys.com/version/stable/>` is not configured."""

    def __init__(self):
        super().__init__("PyPIM is not configured.")


HOST_PORT = 50000


def _get_host_port():
    global HOST_PORT
    HOST_PORT += 1
    return HOST_PORT


def _get_host_path():
    user_data_path = platformdirs.user_data_dir(
        appname="ansys_fluent_core", appauthor="Ansys"
    )
    return os.path.join(user_data_path, "examples")


class FiletransferStrategy(Protocol):
    """File transfer strategy."""

    def upload(
        self, file_name: Union[list[str], str], remote_file_name: Optional[str] = None
    ) -> None:
        """Upload file to the server."""
        ...

    def download(
        self, file_name: Union[list[str], str], local_directory: Optional[str] = None
    ) -> None:
        """Download file from the server."""
        ...


class LocalFileTransferStrategy(FiletransferStrategy):
    """Local file transfer strategy."""

    def __init__(self):
        self.fluent_cwd = (
            pathlib.Path(str(get_fluent_exe_path()).split("fluent")[0]) / "fluent"
        )

    def upload(
        self, file_name: Union[list[str], str], remote_file_name: Optional[str] = None
    ) -> None:
        local_file_name = pathlib.Path(file_name)
        if local_file_name.exists() and local_file_name.is_file():
            if remote_file_name:
                shutil.copyfile(file_name, str(self.fluent_cwd / f"{remote_file_name}"))
            else:
                shutil.copyfile(file_name, str(self.fluent_cwd / f"{file_name}"))

    def download(
        self, file_name: Union[list[str], str], local_directory: Optional[str] = None
    ) -> None:
        dest_path = pathlib.Path(os.getcwd()) / f"{file_name}"
        local_file_name = (
            pathlib.Path(local_directory) if local_directory else dest_path
        )
        if local_file_name.exists() and local_file_name.samefile(file_name):
            return
        shutil.copyfile(file_name, str(local_file_name))


def _get_files(file_name: str):
    if isinstance(file_name, str):
        files = [file_name]
    elif isinstance(
        file_name,
        (
            pathlib.Path,
            pathlib.PurePath,
            pathlib.PosixPath,
            pathlib.PurePosixPath,
            pathlib.WindowsPath,
            pathlib.PureWindowsPath,
        ),
    ):
        files = [str(file_name)]
    elif isinstance(file_name, list):
        files = [str(file) for file in file_name]
    return files


class RemoteFileTransferStrategy(FiletransferStrategy):
    """Provides a file transfer service based on ``gRPC client<https://filetransfer.tools.docs.pyansys.com/version/stable/>``
    and ``gRPC server<https://filetransfer-server.tools.docs.pyansys.com/version/stable/>``
    """

    def __init__(self):
        self.host_port = _get_host_port()
        self.server = subprocess.Popen(
            f"docker run -p {self.host_port}:50000 -v {_get_host_path()}:/home/container/workdir/ -w {_get_host_path()} ghcr.io/ansys/tools-filetransfer:latest",
            shell=True,
        )
        self.client = ft.Client.from_server_address(f"localhost:{self.host_port}")

    def upload(
        self, file_name: Union[list[str], str], remote_file_name: Optional[str] = None
    ):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            File name
        remote_file_name : str, optional
            remote file name, by default None

        Raises
        ------
        FileNotFoundError
            If a file does not exist.
        """
        files = _get_files(file_name)
        if self.client:
            for file in files:
                if os.path.isfile(file):
                    self.client.upload_file(
                        local_filename=file,
                        remote_filename=(
                            remote_file_name
                            if remote_file_name
                            else os.path.basename(file)
                        ),
                    )
                else:
                    raise FileNotFoundError(f"{file} does not exist.")

    def download(
        self, file_name: Union[list[str], str], local_directory: Optional[str] = None
    ):
        """Download a file from the server.

        Parameters
        ----------
        file_name : str
            File name
        local_directory : str, optional
            local directory, by default None.
        """
        files = _get_files(file_name)
        if self.client:
            for file in files:
                if os.path.isfile(file):
                    print(f"\nFile already exists. File path:\n{file}\n")
                else:
                    self.client.download_file(
                        remote_filename=os.path.basename(file),
                        local_filename=(
                            local_directory
                            if local_directory
                            else os.path.basename(file)
                        ),
                    )


class PimFileTransferService:
    """Provides a file transfer service based on ``PyPIM<https://pypim.docs.pyansys.com/version/stable/>`` and ``simple_upload_server()``.

    Attributes
    ----------
    pim_instance: PIM instance
        Instance of PIM which supports upload server services.

    file_service: Client instance
        Instance of Client which supports upload and download methods.

    Methods
    -------
    upload(
        file_name, remote_file_name
        )
        Upload a file to the server.

    download(
        file_name, local_directory
        )
        Download a file from the server.
    """

    def __init__(self, pim_instance: Optional[Any] = None):
        self.pim_instance = pim_instance
        self.upload_server = None
        self.file_service = None
        try:
            if "http-simple-upload-server" in self.pim_instance.services:
                self.upload_server = self.pim_instance.services[
                    "http-simple-upload-server"
                ]
            elif "grpc" in self.pim_instance.services:
                self.upload_server = self.pim_instance.services["grpc"]
        except (AttributeError, KeyError):
            pass
        else:
            try:
                from simple_upload_server.client import Client

                self.file_service = Client(
                    token="token",
                    url=self.upload_server.uri,
                    headers=self.upload_server.headers,
                )
            except ModuleNotFoundError:
                pass

    @property
    def pim_service(self):
        """PIM file transfer service."""
        return self.file_service

    def is_configured(self):
        """Check pypim configuration."""
        return pypim.is_configured()

    def upload_file(self, file_name: str, remote_file_name: Optional[str] = None):
        """Upload a file to the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        remote_file_name : str, optional
            remote file name, by default None

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        PyPIMConfigurationError
            If PyPIM is not configured.
        """
        if not self.is_configured():
            raise PyPIMConfigurationError()
        elif self.file_service:
            if os.path.isfile(file_name):
                expanded_file_path = os.path.expandvars(file_name)
                upload_file_name = remote_file_name or os.path.basename(
                    expanded_file_path
                )
                self.file_service.upload_file(expanded_file_path, upload_file_name)
            else:
                raise FileNotFoundError(f"{file_name} does not exist.")

    def upload(
        self, file_name: Union[list[str], str], remote_file_name: Optional[str] = None
    ):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            File name
        remote_file_name : str, optional
            remote file name, by default None

        Raises
        ------
        FileNotFoundError
            If a file does not exist.
        """
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
            with alive_bar(len(files), title="Uploading...") as bar:
                for file in files:
                    if os.path.isfile(file):
                        if not self.file_service.file_exist(os.path.basename(file)):
                            self.upload_file(
                                file_name=file, remote_file_name=remote_file_name
                            )
                            bar()
                        else:
                            print(f"\n{file} already uploaded.\n")
                    elif not self.file_service.file_exist(os.path.basename(file)):
                        raise FileNotFoundError(f"{file} does not exist.")

    def download_file(self, file_name: str, local_directory: Optional[str] = None):
        """Download a file from the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        local_directory : str, optional
            local directory, by default None

        Raises
        ------
        FileNotFoundError
            If the remote file does not exist.
        PyPIMConfigurationError
            If PyPIM is not configured.
        """
        if not self.is_configured():
            raise PyPIMConfigurationError()
        elif self.file_service:
            if self.file_service.file_exist(file_name):
                self.file_service.download_file(file_name, local_directory)
            else:
                raise FileNotFoundError("Remote file does not exist.")

    def download(
        self, file_name: Union[list[str], str], local_directory: Optional[str] = "."
    ):
        """Download a file from the server.

        Parameters
        ----------
        file_name : str
            File name
        local_directory : str, optional
            local directory, by default current working directory.
        """
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
            with alive_bar(len(files), title="Downloading...") as bar:
                for file in files:
                    if os.path.isfile(file):
                        print(f"\nFile already exists. File path:\n{file}\n")
                    else:
                        self.download_file(
                            file_name=os.path.basename(file),
                            local_directory=local_directory,
                        )
                        bar()

    def __call__(self, pim_instance: Optional[Any] = None):
        self.pim_instance = pim_instance
