from pathlib import Path

from ansys.fluent.core.examples.downloads import get_default_save_path


def rename_downloaded_file(file_path: str, suffix: str) -> str:
    """Rename downloaded file by appending a suffix to the file name.

    Parameters
    ----------
    file_path : str
        Downloaded file path. Can be absolute or relative.
    suffix : str
        Suffix to append to the file name.

    Returns:
    --------
    str
        New file path with the suffix appended to the file name.
    """
    ext = "".join(Path(file_path).suffixes)
    orig_path = Path(file_path)
    file_path = file_path.removesuffix(ext)
    file_path = Path(file_path)
    save_path = get_default_save_path()
    if file_path.is_absolute():
        new_stem = f"{file_path.stem}{suffix}"
        new_path = file_path.with_stem(new_stem)
        new_path = new_path.with_suffix(ext)
        orig_path.rename(new_path)
        return str(new_path)
    else:
        orig_abs_path = Path(save_path) / orig_path
        abs_path = Path(save_path) / file_path
        new_stem = f"{file_path.stem}{suffix}"
        new_path = abs_path.with_stem(new_stem)
        new_path = new_path.with_suffix(ext)
        orig_abs_path.rename(new_path)
        return str(file_path.with_stem(new_stem).with_suffix(ext))
