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
    """Delete all downloaded examples from the default examples folder to free space or
    update the files.

    Notes
    -----
    The default examples path is given by ``pyfluent.EXAMPLES_PATH``.
    """
    shutil.rmtree(pyfluent.EXAMPLES_PATH)
    os.makedirs(pyfluent.EXAMPLES_PATH)


def _decompress(file_name: str) -> None:
    """Decompress zipped file."""
    zip_ref = zipfile.ZipFile(file_name, "r")
    zip_ref.extractall(pyfluent.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(file_name: str, directory: Optional[str] = None) -> str:
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
    save_path: Optional[str] = None,
    return_without_path: Optional[bool] = False,
) -> str:
    """Download specified file from specified URL."""
    file_name = os.path.basename(file_name)
    if save_path is None:
        save_path = pyfluent.EXAMPLES_PATH
    else:
        save_path = os.path.abspath(save_path)
    local_path = os.path.join(save_path, file_name)
    local_path_no_zip = re.sub(".zip$", "", local_path)
    file_name_no_zip = re.sub(".zip$", "", file_name)
    # First check if file has already been downloaded
    print("Checking if specified file already exists...")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        print(f"File already exists. File path:\n{local_path_no_zip}")
        if return_without_path:
            return file_name_no_zip
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
        file_name = file_name_no_zip
    print(f"Download successful. File path:\n{local_path}")
    if return_without_path:
        return file_name
    else:
        return local_path


def download_file(
    file_name: str,
    directory: Optional[str] = None,
    save_path: Optional[str] = None,
    return_without_path: Optional[bool] = None,
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
        if os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1":
            return_without_path = True
        else:
            return_without_path = False

    url = _get_file_url(file_name, directory)
    return _retrieve_file(url, file_name, save_path, return_without_path)


def path(file_name: str):
    if os.path.isabs(file_name):
        return file_name
    file_path = Path(pyfluent.EXAMPLES_PATH) / file_name
    if file_path.is_file():
        return str(file_path)
    else:
        raise FileNotFoundError(f"{file_name} does not exist.")
