from pathlib import Path
from typing import Optional

from ansys.fluent.core import EXAMPLES_PATH


def rename_downloaded_file(
    file_path: str, suffix: str, ext: Optional[str] = None
) -> str:
    """Rename downloaded file by appending a suffix to the file name.

    Parameters
    ----------
    file_path : str
        Downloaded file path. Can be absolute or relative.
    suffix : str
        Suffix to append to the file name.
    ext : str, optional
        Extension of the file, by default None. Must be provided if the file has multiple extensions (e.g. .cas.gz).

    Returns:
    --------
    str
        New file path with the suffix appended to the file name.
    """
    orig_path = Path(file_path)
    if ext:
        file_path = file_path.removesuffix(ext)
    file_path = Path(file_path)
    if file_path.is_absolute():
        new_stem = f"{file_path.stem}_{suffix}"
        new_path = file_path.with_stem(new_stem)
        if ext:
            new_path = new_path.with_suffix(ext)
        orig_path.rename(new_path)
        return str(new_path)
    else:
        orig_abs_path = Path(EXAMPLES_PATH) / orig_path
        abs_path = Path(EXAMPLES_PATH) / file_path
        new_stem = f"{file_path.stem}_{suffix}"
        new_path = abs_path.with_stem(new_stem)
        if ext:
            new_path = new_path.with_suffix(ext)
        orig_abs_path.rename(new_path)
        if ext:
            return str(file_path.with_stem(new_stem).with_suffix(ext))
        else:
            return str(file_path.with_stem(new_stem))
