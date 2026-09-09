# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Functions to download sample datasets from the Ansys example data repository."""

import os
from pathlib import Path
import shutil
import zipfile

import ansys.fluent.core as pyfluent
from ansys.fluent.core._types import PathType
from ansys.tools.common.example_download import download_manager


def delete_downloads():
    """Delete all downloaded examples from the default examples folder to free space or
    update the files.

    Notes
    -----
    The default examples path is given by ``pyfluent.config.examples_path``.
    """
    shutil.rmtree(pyfluent.config.examples_path)
    os.makedirs(pyfluent.config.examples_path)


def _decompress(file_name: str) -> None:
    """Decompress zipped file."""
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(pyfluent.config.examples_path)


def download_file(
    file_name: str,
    directory: str | None = None,
    save_path: "PathType | None" = None,
    return_without_path: bool | None = None,
    force: bool = False,
    timeout: float = 60.0,
    max_retries: int = 3,
) -> str:
    """Download specified example file from the Ansys example data repository.

    Thin wrapper around
    :meth:`ansys.tools.common.example_download.DownloadManager.download_file`
    that flattens the nested ``save_path/directory/file_name`` layout used by
    ``DownloadManager`` to ``save_path/file_name`` and decompresses ``.zip``
    archives, preserving the on-disk layout used in earlier pyfluent releases.

    Parameters
    ----------
    file_name : str
        Name of the example file to download.
    directory : str
        Path under the ``example-data`` repository.
    save_path : str, optional
        Path to download the file to. Defaults to
        ``pyfluent.config.container_mount_source`` if set, otherwise the current
        working directory.
    return_without_path : bool, optional
        When unspecified, defaults to ``False``, unless
        ``pyfluent.config.launch_fluent_container`` is set to ``True`` and
        ``pyfluent.config.use_file_transfer_service`` is not, in which case it
        defaults to ``True``. This is used with Fluent Docker container images so
        that only the file name is returned when Fluent inside the container
        expects it to be accessed relative to its own working directory.
    force : bool, default: False
        Whether to always download the example file. The default is
        ``False``, in which case if the example file is cached, it
        is reused.
    timeout : float, default: 60.0
        Timeout in seconds for each git or HTTP operation attempt (not
        a bound on the total call duration). The default is 60 seconds.
    max_retries : int, default: 3
        Maximum number of retry attempts for failed downloads, applied
        separately to the Git-based and HTTP-based strategies. Between
        attempts, an exponential backoff delay (1, 2, 4, ... seconds) is
        applied. Because this method can fully exhaust retries for the
        Git-based strategy before falling back to the HTTP-based one,
        the worst-case total duration is roughly
        ``2 * max_retries * timeout`` plus the backoff delays for both
        strategies.

    Returns
    -------
    str
        File path of the downloaded or already existing file, or only the file
        name if ``return_without_path=True``.

    Examples
    --------
    >>> from ansys.fluent.core import examples
    >>> file_path = examples.download_file("bracket.iges", "geometry")
    >>> file_path
    '/home/user/.local/share/ansys_fluent_core/examples/bracket.iges'
    >>> file_name = examples.download_file("bracket.iges", "geometry", return_without_path=True)
    >>> file_name
    'bracket.iges'
    >>> file_path = examples.download_file("bracket.iges", "geometry", save_path='.')
    '/home/<current_folder_path>/bracket.iges'
    >>> file_name = examples.download_file("bracket.iges", "geometry", save_path='.', return_without_path=True)
    >>> file_name
    'bracket.iges'
    >>> file_path = examples.download_file("bracket.iges", "geometry", save_path='<user_specified_path>')
    '/home/<user_specified_path>/bracket.iges'
    >>> file_name = examples.download_file("bracket.iges", "geometry", save_path='<user_specified_path>',
    ...                                   return_without_path=True)
    >>> file_name
    'bracket.iges'
    """
    if return_without_path is None:
        return_without_path = (
            pyfluent.config.launch_fluent_container
            and not pyfluent.config.use_file_transfer_service
        )

    file_name = os.path.basename(file_name)
    if save_path is None:
        save_path = pyfluent.config.container_mount_source or os.getcwd()
    save_path = os.path.abspath(save_path)

    local_path = os.path.join(save_path, file_name)
    unzipped_path = local_path[:-4] if local_path.endswith(".zip") else local_path

    # DownloadManager caches under its nested path, so also check the flat path here.
    if not force and os.path.exists(unzipped_path):
        return os.path.basename(unzipped_path) if return_without_path else unzipped_path

    downloaded_path = download_manager.download_file(
        filename=file_name,
        directory=directory or "",
        destination=save_path,
        force=force,
        timeout=timeout,
        max_retries=max_retries,
    )

    if os.path.abspath(downloaded_path) != local_path:
        shutil.move(downloaded_path, local_path)

    if local_path.endswith(".zip"):
        _decompress(local_path)
        local_path = unzipped_path
    return os.path.basename(local_path) if return_without_path else local_path


def path(file_name: str):
    """Return path of given file name.

    Parameters
    ----------
    file_name : str
        Name of the file.

    Raises
    ------
    FileNotFoundError
        If file does not exist.

    Returns
    -------
    file_path: str
        File path.
    """
    if os.path.isabs(file_name):
        return file_name
    file_path = Path(pyfluent.config.examples_path) / file_name
    if file_path.is_file():
        return str(file_path)
    else:
        raise FileNotFoundError(f"{file_name} does not exist.")
