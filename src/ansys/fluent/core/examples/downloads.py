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

"""Functions to download sample datasets from the Ansys example data repository."""

import logging
import os
from pathlib import Path
import re
import shutil
import zipfile

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.networking import check_url_exists, get_url_content

logger = logging.getLogger("pyfluent.networking")


class RemoteFileNotFoundError(FileNotFoundError):
    """Raised on an attempt to download a non-existent remote file."""

    def __init__(self, url):
        """Initializes RemoteFileNotFoundError."""
        super().__init__(f"{url} does not exist.")


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
    zip_ref = zipfile.ZipFile(file_name, "r")
    zip_ref.extractall(pyfluent.config.examples_path)
    return zip_ref.close()


def _get_file_url(file_name: str, directory: str | None = None) -> str:
    """Get file URL."""
    if directory:
        return (
            "https://github.com/ansys/example-data/raw/master/"
            f"{directory}/{file_name}"
        )
    return f"https://github.com/ansys/example-data/raw/master/{file_name}"


def _retrieve_file(
    url: str,
    file_name: str,
    save_path: str | None = None,
    return_without_path: bool | None = False,
) -> str:
    """Download specified file from specified URL."""
    file_name = os.path.basename(file_name)
    if save_path is None:
        save_path = pyfluent.config.container_mount_source or os.getcwd()
    else:
        save_path = os.path.abspath(save_path)
    local_path = os.path.join(save_path, file_name)
    local_path_no_zip = re.sub(".zip$", "", local_path)
    file_name_no_zip = re.sub(".zip$", "", file_name)
    # First check if file has already been downloaded
    logger.info(f"Checking if {local_path_no_zip} already exists...")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        logger.info("File already exists.")
        if return_without_path:
            return file_name_no_zip
        else:
            return local_path_no_zip

    logger.info("File does not exist. Downloading specified file...")

    # Check if save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Download file
    logger.info(f'Downloading URL: "{url}"')
    content = get_url_content(url)
    with open(local_path, "wb") as f:
        f.write(content)

    if local_path.endswith(".zip"):
        _decompress(local_path)
        local_path = local_path_no_zip
        file_name = file_name_no_zip
    logger.info("Download successful.")
    if return_without_path:
        return file_name
    else:
        return local_path


def download_file(
    file_name: str,
    directory: str | None = None,
    save_path: str | None = None,
    return_without_path: bool | None = None,
) -> str:
    """Download specified example file from the Ansys example data repository.

    Parameters
    ----------
    file_name : str
        File to download.
    directory : str, optional
        Ansys example data repository directory where specified file is located. If not specified, looks for the file
        in the root directory of the repository.
    save_path : str, optional
        Path to download the specified file to.
    return_without_path : bool, optional
        When unspecified, defaults to False, unless the PYFLUENT_LAUNCH_CONTAINER=1 environment variable is specified,
        in which case defaults to True.
        Relevant when using Fluent Docker container images, as the full path for the imported file from
        the host side is not necessarily going to be the same as the one for Fluent inside the container.
        Assuming the Fluent inside the container has its working directory set to the path that was mounted from
        the host, and that the example files are being made available by the host through this same path,
        only the file name is required for Fluent to find and open the file.

    Raises
    ------
    RemoteFileNotFoundError
        If remote file does not exist.

    Returns
    -------
    str
        file path of the downloaded or already existing file, or only the file name if ``return_without_path=True``.

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
        if pyfluent.config.launch_fluent_container:
            if pyfluent.config.use_file_transfer_service:
                return_without_path = False
            else:
                return_without_path = True

    url = _get_file_url(file_name, directory)
    if not check_url_exists(url):
        raise RemoteFileNotFoundError(url)
    return _retrieve_file(url, file_name, save_path, return_without_path)


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
