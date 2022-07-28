"""Functions to download sample datasets from the PyAnsys data repository.

Examples
--------

>>> from ansys.fluent.core import examples
>>> filename = examples.download_file("bracket.iges", "geometry")
>>> filename
'/home/user/.local/share/ansys_fluent_core/examples/bracket.iges'
"""
import os
import shutil
from typing import Optional
import urllib.request
import zipfile

import ansys.fluent.core as pyfluent


def get_ext(filename: str) -> str:
    """Extract the extension of a file."""
    ext = os.path.splitext(filename)[1].lower()
    return ext


def delete_downloads() -> bool:
    """Delete all downloaded examples to free space or update the files."""
    shutil.rmtree(pyfluent.EXAMPLES_PATH)
    os.makedirs(pyfluent.EXAMPLES_PATH)
    return True


def _decompress(filename: str) -> None:
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(pyfluent.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(filename: str, directory: Optional[str] = None) -> str:
    if directory:
        return (
            "https://github.com/pyansys/example-data/raw/master/"
            f"{directory}/{filename}"
        )
    return f"https://github.com/pyansys/example-data/raw/master/{filename}"


def _retrieve_file(url: str, filename: str):
    # First check if file has already been downloaded
    local_path = os.path.join(pyfluent.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip, None

    # grab the correct url retriever
    urlretrieve = urllib.request.urlretrieve

    # Perform download
    saved_file, resp = urlretrieve(url)
    shutil.move(saved_file, local_path)
    if get_ext(local_path) in [".zip"]:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path, resp


def download_file(filename: str, directory: Optional[str] = None):
    url = _get_file_url(filename, directory)
    return _retrieve_file(url, filename)[0]
