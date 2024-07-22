from pathlib import Path
import shutil

import pytest

from ansys.fluent.core import EXAMPLES_PATH
from tests.util import rename_downloaded_file


@pytest.mark.parametrize(
    "ext,a,b,c,d",
    [(".cas", "a1", "b1", "c1", "d1"), (".cas.gz", "a2", "b2", "c2", "d2")],
)
def test_rename_downloaded_file(ext, a, b, c, d):
    try:
        file_path = Path(EXAMPLES_PATH) / f"{a}{ext}"
        file_path.touch()
        file_path = str(file_path)
        new_file_path = rename_downloaded_file(file_path, "_1")
        assert new_file_path == str(Path(EXAMPLES_PATH) / f"{a}_1{ext}")
    except Exception:
        raise
    finally:
        Path(new_file_path).unlink(missing_ok=True)

    try:
        file_path = f"{b}{ext}"
        (Path(EXAMPLES_PATH) / file_path).touch()
        new_file_path = rename_downloaded_file(file_path, "_1")
        assert new_file_path == f"{b}_1{ext}"
    except Exception:
        raise
    finally:
        (Path(EXAMPLES_PATH) / new_file_path).unlink(missing_ok=True)

    try:
        dir_path = Path(EXAMPLES_PATH) / c
        dir_path.mkdir()
        file_path = dir_path / f"{d}{ext}"
        file_path.touch()
        file_path = str(Path(c) / f"{d}{ext}")
        new_file_path = rename_downloaded_file(file_path, "_1")
        assert new_file_path == str(Path(c) / f"{d}_1{ext}")
    except Exception:
        raise
    finally:
        shutil.rmtree(dir_path, ignore_errors=True)
