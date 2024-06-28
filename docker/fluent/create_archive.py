"""Provides a module to create an archive of Fluent unified installation."""

import os
from pathlib import Path
import shutil
from typing import Union

current_path = Path(__file__.rstrip(os.path.basename(__file__)))


def create_file_folders_list(files_list: list):
    """Create a list of files and folders specified in a text file.

    Parameters
    ----------
    files_list: list
        List of text files containing relative paths of files and folders.

    Returns
    -------
    file_folders: list
        List of files and folders specified in given text files.
    """
    file_folders = []
    for file in files_list:
        with open(Path(current_path) / file, "r") as f:
            lines = f.readlines()
            file_folders.extend([line.rstrip("\n") for line in lines])
    return file_folders


def copy_files(src: Union[Path, str], copy_list: list, remove_list: list):
    """Create an archive from Fluent unified installation.

    Parameters
    ----------
    src: Union[Path, str]
        Path of ``ansys_inc`` folder in Fluent unified installation directory.
    copy_list: list
        List of text files containing relative paths of files and folders to include them in the archive.
    remove_list: list
        List of text files containing relative paths of files and folders to exclude them from the archive.
    """
    dst = Path(current_path) / "ansys_inc"
    for file in copy_list:
        source = Path(src) / file
        destination = Path(dst) / file
        if Path(source).is_file():
            Path(destination).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src=source, dst=destination)
        elif Path(source).is_dir():
            Path(destination).mkdir(parents=True, exist_ok=True)
            shutil.copytree(src=source, dst=destination, dirs_exist_ok=True)
    for file in remove_list:
        destination = Path(dst) / file
        if Path(destination).is_file():
            Path(destination).unlink()
        elif Path(destination).is_dir():
            shutil.rmtree(Path(destination))


if __name__ == "__main__":
    copy_list = ["cadList.txt", "ceiList.txt", "cfdpostList.txt", "fluentList.txt"]
    remove_list = ["excludeCEIList.txt", "excludeFluentList.txt"]
    copy_files(
        src="/<path>/ansys_inc",
        copy_list=create_file_folders_list(files_list=copy_list),
        remove_list=create_file_folders_list(files_list=remove_list),
    )
