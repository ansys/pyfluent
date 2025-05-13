# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module for file transfer service."""

import os
import pathlib
import shutil
from typing import Protocol

from ansys.fluent.core.utils import get_user_data_dir

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


class StandaloneFileTransferStrategy(FileTransferStrategy):
    """Provides the local file transfer strategy can be used for Fluent launched in the
    standalone mode.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> from ansys.fluent.core import examples
    >>> from ansys.fluent.core.utils.file_transfer_service import StandaloneFileTransferStrategy
    >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
    >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=StandaloneFileTransferStrategy())
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
        >>> from ansys.fluent.core.utils.file_transfer_service import StandaloneFileTransferStrategy
        >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
        >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=StandaloneFileTransferStrategy())
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
        >>> from ansys.fluent.core.utils.file_transfer_service import StandaloneFileTransferStrategy
        >>> mesh_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
        >>> meshing_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, file_transfer_service=StandaloneFileTransferStrategy())
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
