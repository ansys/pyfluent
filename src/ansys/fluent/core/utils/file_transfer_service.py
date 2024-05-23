"""Provides a module for file transfer service."""

import logging
import os
import pathlib
import random
import shutil
from typing import Any, Callable, List, Optional, Protocol, Union  # noqa: F401
import warnings

from alive_progress import alive_bar

import ansys.fluent.core as pyfluent
from ansys.fluent.core.warnings import PyFluentUserWarning
import ansys.platform.instancemanagement as pypim
import ansys.tools.filetransfer as ft
import docker

logger = logging.getLogger("pyfluent.file_transfer_service")


class PyPIMConfigurationError(ConnectionError):
    """Raised when `PyPIM<https://pypim.docs.pyansys.com/version/stable/>` is not configured."""

    def __init__(self):
        super().__init__("PyPIM is not configured.")


class FileTransferStrategy(Protocol):
    """Provides the file transfer strategy."""

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


class LocalFileTransferStrategy(FileTransferStrategy):
    """Provides the local file transfer strategy."""

    def __init__(self, server_cwd: Optional[str] = None):
        """Local File Transfer Service.

        Parameters
        ----------
        server_cwd: str, Optional
            Current working directory of server/Fluent.
        """
        self.pyfluent_cwd = pathlib.Path(str(os.getcwd()))
        self.fluent_cwd = (
            pathlib.Path(str(server_cwd)) if server_cwd else self.pyfluent_cwd
        )

    def file_exists_on_remote(self, file_name: str) -> bool:
        """Check if remote file exists.

        Parameters
        ----------
        file_name: str
            File name.

        Returns
        -------
            Whether file exists.
        """
        full_file_name = pathlib.Path(self.fluent_cwd) / os.path.basename(file_name)
        return full_file_name.is_file()

    def upload(
        self, file_name: Union[list[str], str], remote_file_name: Optional[str] = None
    ) -> None:
        local_file_name = pathlib.Path(file_name)
        if local_file_name.exists() and local_file_name.is_file():
            if remote_file_name:
                shutil.copyfile(
                    file_name,
                    str(self.fluent_cwd / f"{os.path.basename(remote_file_name)}"),
                )
            else:
                shutil.copyfile(
                    file_name, str(self.fluent_cwd / f"{os.path.basename(file_name)}")
                )

    def download(
        self, file_name: Union[list[str], str], local_directory: Optional[str] = None
    ) -> None:
        remote_file_name = str(self.fluent_cwd / f"{os.path.basename(file_name)}")
        local_file_name = None
        if local_directory:
            if pathlib.Path(local_directory).is_dir():
                local_file_name = pathlib.Path(local_directory) / os.path.basename(
                    file_name
                )
            elif not pathlib.Path(local_directory).is_dir():
                local_file_name = pathlib.Path(local_directory)
        else:
            local_file_name = pathlib.Path(self.pyfluent_cwd) / os.path.basename(
                file_name
            )
        if local_file_name.exists() and local_file_name.samefile(remote_file_name):
            return
        shutil.copyfile(remote_file_name, str(local_file_name))


def _get_files(
    file_name: Union[str, pathlib.PurePath, list[Union[str, pathlib.PurePath]]],
):
    if isinstance(file_name, (str, pathlib.PurePath)):
        files = [pathlib.Path(file_name)]
    elif isinstance(file_name, list):
        files = [pathlib.Path(file) for file in file_name]
    return files


class RemoteFileTransferStrategy(FileTransferStrategy):
    """Provides a file transfer service based on the `gRPC client <https://filetransfer.tools.docs.pyansys.com/version/stable/>`_
    and ``gRPC server <https://filetransfer-server.tools.docs.pyansys.com/version/stable/>`_.
    """

    def __init__(
        self,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        port: Optional[int] = None,
        container_mount_path: Optional[str] = None,
        host_mount_path: Optional[str] = None,
    ):
        """Provides the gRPC-based remote file transfer strategy.

        Parameters
        ----------
        image_name: str
            Name of the image.
        image_tag : str, optional
            Tag of the image.
        port: int, optional
            Port for the file transfer service to use.
        container_mount_path: Union[str, Path], optional
            Path inside the container for the host mount path.
        host_mount_path: Union[str, Path], optional
            Existing path in the host operating system to be available inside the container.
        """
        self.docker_client = docker.from_env()
        self.image_name = (
            image_name if image_name else "ghcr.io/ansys/tools-filetransfer"
        )
        self.image_tag = image_tag if image_tag else "latest"
        self.container_mount_path = (
            container_mount_path if container_mount_path else "/home/container/workdir/"
        )
        self.host_mount_path = (
            host_mount_path if host_mount_path else pyfluent.USER_DATA_PATH
        )
        try:
            self.host_port = port if port else random.randint(5000, 6000)
            self.ports = {"50000/tcp": self.host_port}
            self.container = self.docker_client.containers.run(
                image=f"{self.image_name}:{self.image_tag}",
                ports=self.ports,
                detach=True,
                volumes=[f"{self.host_mount_path}:{self.container_mount_path}"],
            )
        except docker.errors.DockerException:
            self.host_port = port if port else random.randint(6000, 7000)
            self.ports = {"50000/tcp": self.host_port}
            self.container = self.docker_client.containers.run(
                image=f"{self.image_name}:{self.image_tag}",
                ports=self.ports,
                detach=True,
                volumes=[f"{self.host_mount_path}:{self.container_mount_path}"],
            )
        self.client = ft.Client.from_server_address(f"localhost:{self.host_port}")

    def file_exists_on_remote(self, file_name: str) -> bool:
        """Check if remote file exists.

        Parameters
        ----------
        file_name: str
            File name.

        Returns
        -------
            Whether file exists.
        """
        full_file_name = pathlib.Path(self.host_mount_path) / os.path.basename(
            file_name
        )
        return full_file_name.is_file()

    def upload(
        self, file_name: Union[list[str], str], remote_file_name: Optional[str] = None
    ):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            File name.
        remote_file_name : str, optional
            Remote file name. The default is ``None``.

        Raises
        ------
        FileNotFoundError
            If a file does not exist.
        """
        files = _get_files(file_name)
        if self.client:
            for file in files:
                is_file_on_remote = self.file_exists_on_remote(os.path.basename(file))
                if is_file_on_remote:
                    warnings.warn(
                        f"\n{file} with the same name exists at the remote location.\n",
                        PyFluentUserWarning,
                    )
                elif os.path.isfile(file) and not is_file_on_remote:
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
            File name.
        local_directory : str, optional
            Local directory. The default is ``None``.
        """
        files = _get_files(file_name)
        if self.client:
            for file in files:
                if os.path.isfile(file):
                    warnings.warn(
                        f"\nFile already exists. File path:\n{file}\n",
                        PyFluentUserWarning,
                    )
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
    """Provides a file transfer service based on `PyPIM <https://pypim.docs.pyansys.com/version/stable/>`_ and the ``simple_upload_server()`` method.

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

    def file_exists_on_remote(self, file_name: str) -> bool:
        """Check if remote file exists.

        Parameters
        ----------
        file_name: str
            File name.

        Returns
        -------
            Whether file exists.
        """
        return self.file_service.file_exist(os.path.basename(file_name))

    def is_configured(self):
        """Check pypim configuration."""
        return pypim.is_configured()

    def upload_file(self, file_name: str, remote_file_name: Optional[str] = None):
        """Upload a file to the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            File name.
        remote_file_name : str, optional
            Remote file name. The default is ``None``.

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
            File name.
        remote_file_name : str, optional
            Remote file name. The default is ``None``.

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
                            warnings.warn(
                                f"\n{file} with the same name exists at the remote location.\n",
                                PyFluentUserWarning,
                            )
                    elif not self.file_service.file_exist(os.path.basename(file)):
                        raise FileNotFoundError(f"{file} does not exist.")

    def download_file(self, file_name: str, local_directory: Optional[str] = None):
        """Download a file from the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            File name.
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
            File name.
        local_directory : str, optional
            Local directory. The default is the current working directory.
        """
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
            with alive_bar(len(files), title="Downloading...") as bar:
                for file in files:
                    if os.path.isfile(file):
                        warnings.warn(
                            f"\nFile already exists. File path:\n{file}\n",
                            PyFluentUserWarning,
                        )
                    else:
                        self.download_file(
                            file_name=os.path.basename(file),
                            local_directory=local_directory,
                        )
                        bar()

    def __call__(self, pim_instance: Optional[Any] = None):
        self.pim_instance = pim_instance
