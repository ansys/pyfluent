"""Provides a module for file transfer service."""

import os
import pathlib
import random
import shutil
from typing import Any, Protocol
import warnings

from ansys.fluent.core.utils import get_user_data_dir
from ansys.fluent.core.utils.deprecate import deprecate_argument
from ansys.fluent.core.warnings import PyFluentUserWarning
import ansys.platform.instancemanagement as pypim

# Host path which is mounted to the file-transfer-service container
MOUNT_SOURCE = str(get_user_data_dir())


class PyPIMConfigurationError(ConnectionError):
    """Raised when `PyPIM<https://pypim.docs.pyansys.com/version/stable/>` is not configured."""

    def __init__(self):
        """Initialize PyPIMConfigurationError."""
        super().__init__("PyPIM is not configured.")


class FileTransferStrategy(Protocol):
    """Provides the file transfer strategy."""

    def upload(
        self, file_name: list[str] | str, remote_file_name: str | None = None
    ) -> None:
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            File name.
        remote_file_name : str, optional
            Remote file name. The default is ``None``.
        """
        ...

    def download(
        self, file_name: list[str] | str, local_directory: str | None = None
    ) -> None:
        """Download a file from the server.

        Parameters
        ----------
        file_name : str
            File name.
        local_directory : str, optional
            Local directory. The default is ``None``.
        """
        ...


class LocalFileTransferStrategy(FileTransferStrategy):
    """Provides the local file transfer strategy can be used for Fluent launched in the
    standalone mode.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> from ansys.fluent.core import examples
    >>> from ansys.fluent.core.utils.file_transfer_service import LocalFileTransferStrategy
    >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
    >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=LocalFileTransferStrategy())
    >>> meshing_session.upload(file_name=mesh_file_name, remote_file_name="elbow.msh.h5")
    >>> meshing_session.meshing.File.ReadMesh(FileName="elbow.msh.h5")
    >>> meshing_session.meshing.File.WriteMesh(FileName="write_elbow.msh.h5")
    >>> meshing_session.download(file_name="write_elbow.msh.h5", local_directory="<local_directory_path>")
    """

    def __init__(self, server_cwd: str | None = None):
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
        self, file_name: list[str] | str, remote_file_name: str | None = None
    ) -> None:
        """Upload a file to the server.

        Parameters
        ----------
        file_name : list[str] | str
            File name.
        remote_file_name : str, optional
            Remote file name. The default is ``None``.

        Raises
        ------
        FileNotFoundError
            If a file does not exist.

        Examples
        --------
        >>> import ansys.fluent.core as pyfluent
        >>> from ansys.fluent.core import examples
        >>> from ansys.fluent.core.utils.file_transfer_service import LocalFileTransferStrategy
        >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
        >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=LocalFileTransferStrategy())
        >>> meshing_session.upload(file_name=mesh_file_name, remote_file_name="elbow.msh.h5")
        >>> meshing_session.meshing.File.ReadMesh(FileName="elbow.msh.h5")
        """
        files = _get_files(file_name)
        for file in files:
            if file.is_file():
                if remote_file_name:
                    shutil.copyfile(
                        file,
                        str(self.fluent_cwd / f"{os.path.basename(remote_file_name)}"),
                    )
                else:
                    shutil.copyfile(
                        file, str(self.fluent_cwd / f"{os.path.basename(file)}")
                    )

    def download(
        self, file_name: list[str] | str, local_directory: str | None = None
    ) -> None:
        """Download a file from the server.

        Parameters
        ----------
        file_name : list[str] | str
            File name.
        local_directory : str, optional
            Local directory. The default is ``None``.

        Examples
        --------
        >>> import ansys.fluent.core as pyfluent
        >>> from ansys.fluent.core import examples
        >>> from ansys.fluent.core.utils.file_transfer_service import LocalFileTransferStrategy
        >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
        >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=LocalFileTransferStrategy())
        >>> meshing_session.meshing.File.WriteMesh(FileName="write_elbow.msh.h5")
        >>> meshing_session.download(file_name="write_elbow.msh.h5", local_directory="<local_directory_path>")
        """
        files = _get_files(file_name)
        for file in files:
            remote_file_name = str(self.fluent_cwd / file.name)
            local_file_name = None
            if local_directory:
                local_dir_path = pathlib.Path(local_directory)
                if local_dir_path.is_dir():
                    local_file_name = local_dir_path / file.name
                else:
                    local_file_name = local_dir_path
            else:
                local_file_name = self.pyfluent_cwd / file.name
            if local_file_name.exists() and local_file_name.samefile(remote_file_name):
                return
            shutil.copyfile(remote_file_name, str(local_file_name))


def _get_files(
    file_name: str | pathlib.PurePath | list[str | pathlib.PurePath],
):
    if isinstance(file_name, (str, pathlib.PurePath)):
        files = [pathlib.Path(file_name)]
    elif isinstance(file_name, list):
        files = [pathlib.Path(file) for file in file_name]
    return files


class RemoteFileTransferStrategy(FileTransferStrategy):
    """Provides a file transfer service based on the `gRPC client <https://filetransfer.tools.docs.pyansys.com/version/stable/>`_
    and `gRPC server <https://filetransfer-server.tools.docs.pyansys.com/version/stable/>`_.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> from ansys.fluent.core import examples
    >>> from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy
    >>> case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    >>> solver_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER, file_transfer_service=RemoteFileTransferStrategy())
    >>> solver_session.upload(file_name=case_file_name, remote_file_name="elbow.cas.h5")
    >>> solver_session.file.read_case(file_name="elbow.cas.h5")
    >>> solver_session.file.write_case(file_name="write_elbow.cas.h5")
    >>> solver_session.download(file_name="write_elbow.cas.h5", local_directory="<local_directory_path>")
    """

    @deprecate_argument("container_mount_path", "mount_target")
    @deprecate_argument("host_mount_path", "mount_source")
    def __init__(
        self,
        image_name: str | None = None,
        image_tag: str | None = None,
        port: int | None = None,
        mount_target: str | None = None,
        mount_source: str | None = None,
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
        mount_target: str | Path, optional
            Path inside the container where ``mount_source`` will be mounted to.
        mount_source: str | Path, optional
            Existing path in the host operating system that will be mounted to ``mount_target``.
        """
        import docker

        self.docker_client = docker.from_env()
        self.image_name = (
            image_name if image_name else "ghcr.io/ansys/tools-filetransfer"
        )
        self.image_tag = image_tag if image_tag else "latest"
        self.mount_target = mount_target if mount_target else "/home/container/workdir/"
        self.mount_source = mount_source if mount_source else MOUNT_SOURCE
        try:
            self.host_port = port if port else random.randint(5000, 6000)
            self.ports = {"50000/tcp": self.host_port}
            self.container = self.docker_client.containers.run(
                image=f"{self.image_name}:{self.image_tag}",
                ports=self.ports,
                detach=True,
                volumes=[f"{self.mount_source}:{self.mount_target}"],
            )
        except docker.errors.DockerException:
            self.host_port = port if port else random.randint(6000, 7000)
            self.ports = {"50000/tcp": self.host_port}
            self.container = self.docker_client.containers.run(
                image=f"{self.image_name}:{self.image_tag}",
                ports=self.ports,
                detach=True,
                volumes=[f"{self.mount_source}:{self.mount_target}"],
            )
        import ansys.tools.filetransfer as ft

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
        full_file_name = pathlib.Path(self.mount_source) / os.path.basename(file_name)
        return full_file_name.is_file()

    def upload(self, file_name: list[str] | str, remote_file_name: str | None = None):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : list[str] | str
            File name.
        remote_file_name : str, optional
            Remote file name. The default is ``None``.

        Raises
        ------
        FileNotFoundError
            If a file does not exist.

        Examples
        --------
        >>> import ansys.fluent.core as pyfluent
        >>> from ansys.fluent.core import examples
        >>> from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy
        >>> case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
        >>> solver_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER, file_transfer_service=RemoteFileTransferStrategy())
        >>> solver_session.upload(file_name=case_file_name, remote_file_name="elbow.cas.h5")
        >>> solver_session.file.read_case(file_name="elbow.cas.h5")
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

    def download(self, file_name: list[str] | str, local_directory: str | None = None):
        """Download a file from the server.

        Parameters
        ----------
        file_name : list[str] | str
            File name.
        local_directory : str, optional
            Local directory. The default is ``None``.

        Examples
        --------
        >>> import ansys.fluent.core as pyfluent
        >>> from ansys.fluent.core import examples
        >>> from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy
        >>> case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
        >>> solver_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER, file_transfer_service=RemoteFileTransferStrategy())
        >>> solver_session.file.write_case(file_name="write_elbow.cas.h5")
        >>> solver_session.download(file_name="write_elbow.cas.h5", local_directory="<local_directory_path>")
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

    def __init__(self, pim_instance: Any | None = None):
        """Initialize PimFileTransferService.

        Parameters
        ----------
        pim_instance: Any, optional
            PIM instance.
        """
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

    def upload_file(self, file_name: str, remote_file_name: str | None = None):
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

    def upload(self, file_name: list[str] | str, remote_file_name: str | None = None):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : list[str] | str
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
            for file in files:
                if os.path.isfile(file):
                    if not self.file_service.file_exist(os.path.basename(file)):
                        self.upload_file(
                            file_name=file, remote_file_name=remote_file_name
                        )
                        print(f"\n{os.path.basename(file_name)} uploaded.\n")
                    else:
                        warnings.warn(
                            f"\n{file} with the same name exists at the remote location.\n",
                            PyFluentUserWarning,
                        )
                elif not self.file_service.file_exist(os.path.basename(file)):
                    raise FileNotFoundError(f"{file} does not exist.")

    def download_file(self, file_name: str, local_directory: str | None = None):
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

    def download(self, file_name: list[str] | str, local_directory: str | None = "."):
        """Download a file from the server.

        Parameters
        ----------
        file_name : list[str] | str
            File name.
        local_directory : str, optional
            Local directory. The default is the current working directory.
        """
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
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
                    print(f"\n{os.path.basename(file_name)} downloaded.\n")

    def __call__(self, pim_instance: Any | None = None):
        self.pim_instance = pim_instance
