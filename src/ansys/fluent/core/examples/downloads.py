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

import ansys.fluent.core as pyfluent
from ansys.fluent.core._types import PathType
from ansys.tools.common.example_download import download_manager


def download_file(
    file_name: str,
    directory: str | None = None,
    save_path: "PathType | None" = None,
    return_without_path: bool | None = None,
    force: bool = False,
    timeout: float = 60,
    max_retries: int = 3,
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
        When unspecified, defaults to False, unless the launch_fluent_container config is set to True,
        in which case defaults to True.
        Relevant when using Fluent Docker container images, as the full path for the imported file from
        the host side is not necessarily going to be the same as the one for Fluent inside the container.
        Assuming the Fluent inside the container has its working directory set to the path that was mounted from
        the host, and that the example files are being made available by the host through this same path,
        only the file name is required for Fluent to find and open the file.
    force : bool, optional
        Whether to always download the example file. The default is False, in which case if the example file is cached, it is reused.
    timeout : float, optional
        Timeout in seconds for the download operation. The default is 60 seconds.
    max_retries: int, optional
        Maximum number of retry attempts for failed downloads. The default is 3.

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

    local_path = download_manager.download_file(
        file_name,
        directory,
        destination=Path.cwd() if save_path == "." else save_path,
        force=force,
        timeout=timeout,
        max_retries=max_retries,
    )

    if return_without_path:
        return Path(local_path).name
    return local_path


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
