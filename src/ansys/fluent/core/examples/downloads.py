"""Functions to download sample datasets from the Ansys example data repository."""
import os
from pathlib import Path
import re
import shutil
from typing import Optional
import urllib.request
import zipfile

import ansys.fluent.core as pyfluent


def delete_downloads():
    """Delete all downloaded examples from the default examples folder to free space or update the files.

    Notes
    -----
    The default examples path is given by ``pyfluent.EXAMPLES_PATH``."""
    shutil.rmtree(pyfluent.EXAMPLES_PATH)
    os.makedirs(pyfluent.EXAMPLES_PATH)


def _decompress(filename: str) -> None:
    """Decompress zipped file."""
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(pyfluent.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(filename: str, directory: Optional[str] = None) -> str:
    """Get file URL."""
    if directory:
        return (
            "https://github.com/ansys/example-data/raw/master/"
            f"{directory}/{filename}"
        )
    return f"https://github.com/ansys/example-data/raw/master/{filename}"


def _retrieve_file(
    url: str,
    filename: str,
    save_path: Optional[str] = None,
    return_only_filename: Optional[bool] = False,
) -> str:
    """Download specified file from specified URL."""
    filename = os.path.basename(filename)
    if save_path is None:
        save_path = pyfluent.EXAMPLES_PATH
    else:
        save_path = os.path.abspath(save_path)
    local_path = os.path.join(save_path, filename)
    local_path_no_zip = re.sub(".zip$", "", local_path)
    filename_no_zip = re.sub(".zip$", "", filename)
    # First check if file has already been downloaded
    print("Checking if specified file already exists...")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        print(f"File already exists. File path:\n{local_path_no_zip}")
        if return_only_filename:
            return filename_no_zip
        else:
            return local_path_no_zip

    print("File does not exist. Downloading specified file...")

    # Check if save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # grab the correct url retriever
    urlretrieve = urllib.request.urlretrieve

    # Perform download
    urlretrieve(url, filename=local_path)
    if local_path.endswith(".zip"):
        _decompress(local_path)
        local_path = local_path_no_zip
        filename = filename_no_zip
    print(f"Download successful. File path:\n{local_path}")
    if return_only_filename:
        return filename
    else:
        return local_path


def download_file(
    filename: str,
    directory: Optional[str] = None,
    save_path: Optional[str] = None,
    return_only_filename: Optional[bool] = None,
) -> str:
    """Download specified example file from the Ansys example data repository.

    Parameters
    ----------
    filename : str
        File to download.
    directory : str, optional
        Ansys example data repository directory where specified file is located. If not specified, looks for the file
        in the root directory of the repository.
    save_path : str, optional
        Path to download the specified file to.
    return_only_filename : bool, optional
        When unspecified, defaults to False, unless the PYFLUENT_LAUNCH_CONTAINER=1 environment variable is specified,
        in which case defaults to True.
        Relevant when using Fluent Docker container images, as the full path for the imported file from
        the host side is not necessarily going to be the same as the one for Fluent inside the container.
        Assuming the Fluent inside the container has its working directory set to the path that was mounted from
        the host, and that the example files are being made available by the host through this same path,
        only the filename is required for Fluent to find and open the file.

    Returns
    -------
    str
        Filepath of the downloaded or already existing file, or only the file name if ``return_only_filename=True``.

    Examples
    --------
    >>> from ansys.fluent.core import examples
    >>> filepath = examples.download_file("bracket.iges", "geometry")
    >>> filepath
    '/home/user/.local/share/ansys_fluent_core/examples/bracket.iges'
    >>> filename = examples.download_file("bracket.iges", "geometry", return_only_filename=True)
    >>> filename
    'bracket.iges'
    """
    if return_only_filename is None:
        if os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1":
            return_only_filename = True
        else:
            return_only_filename = False

    url = _get_file_url(filename, directory)
    return _retrieve_file(url, filename, save_path, return_only_filename)


def path(filename: str):
    if os.path.isabs(filename):
        return filename
    file_path = Path(pyfluent.EXAMPLES_PATH) / filename
    if file_path.is_file():
        return str(file_path)
    else:
        raise FileNotFoundError(f"{filename} does not exist.")
