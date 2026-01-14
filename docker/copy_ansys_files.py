"""Provides a module to copy files from the Ansys installation directory."""

from pathlib import Path
import shutil
import sys


def create_file_folders_list(files_list: list, fluent_version: Path | str):
    """Create a list of files and folders specified in a text file.

    Parameters
    ----------
    files_list: list
        List of text files containing relative paths of files and folders.
    fluent_version: Path | str
        Path of ``docker/fluent_<version>`` folder.

    Returns
    -------
    file_folders: list
        List of files and folders specified in given text files.
    """
    file_folders = []
    for file in files_list:
        with open(Path(fluent_version) / file) as f:
            lines = f.readlines()
            file_folders.extend([line.rstrip("\n") for line in lines])
    return file_folders


def copy_files(src: Path | str, fluent_version: Path | str, mode: str | None = None):
    """Copy files from the Ansys installation directory.

    Parameters
    ----------
    src: Path | str
        Path of ``ansys_inc`` folder in the Ansys installation directory.
    fluent_version: Path | str
        Path of ``docker/fluent_<version>`` folder.
    mode: str | None
        Optional mode selector. Supported values: ``"solver"``, ``"meshing"``.
        If not provided or invalid, uses the default which includes all lists.
    """
    # Determine which list files to use based on mode
    mode_key = (mode or "default").lower()
    copy_map = {
        "solver": ["ceiList.txt", "cfdpostList.txt", "fluentList.txt"],
        "meshing": ["cadList.txt", "fluentList.txt"],
        "default": [
            "cadList.txt",
            "ceiList.txt",
            "cfdpostList.txt",
            "fluentList.txt",
        ],
    }
    remove_map = {
        "solver": ["excludeCEIList.txt", "excludeFluentList.txt"],
        "meshing": ["excludeFluentList.txt"],
        "default": ["excludeCEIList.txt", "excludeFluentList.txt"],
    }

    # Fallback to default if mode is unrecognized
    copy_files = copy_map.get(mode_key, copy_map["default"])
    remove_files = remove_map.get(mode_key, remove_map["default"])

    # Only include list files that exist in the target directory
    copy_files = [f for f in copy_files if (Path(fluent_version) / f).exists()]
    remove_files = [f for f in remove_files if (Path(fluent_version) / f).exists()]
    copy_list = create_file_folders_list(
        files_list=copy_files, fluent_version=fluent_version
    )
    remove_list = create_file_folders_list(
        files_list=remove_files, fluent_version=fluent_version
    )
    dst = Path(fluent_version) / "ansys_inc"
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
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: python copy_ansys_files.py <path to ansys_inc> <path to docker/fluent_<version>> [solver|meshing]"
        )
    mode = sys.argv[3] if len(sys.argv) > 3 else None
    copy_files(src=sys.argv[1], fluent_version=sys.argv[2], mode=mode)
