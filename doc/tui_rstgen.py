"""Provides a module for generating Fluent TUI result files."""

import fnmatch
import os
from pathlib import Path
import shutil

_THIS_DIR = Path(__file__).parent

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_tui_docdir(mode: str):
    return os.path.normpath(
        os.path.join(
            _THIS_DIRNAME,
            "..",
            "doc",
            "source",
            "api",
            mode,
            "tui",
        )
    )


def _get_tui_filepath(mode: str):
    return os.path.normpath(
        os.path.join(
            _THIS_DIRNAME,
            "..",
            "src",
            "ansys",
            "fluent",
            "core",
            f"{mode}",
        )
    )


def _get_tui_file_name(mode: str):
    for file in os.listdir(_get_tui_filepath(mode)):
        if fnmatch.fnmatch(file, "tui_*.py"):
            return file


def generate():
    """Generates TUI .rst files"""
    for mode in ["meshing", "solver"]:
        if Path(_get_tui_docdir(mode)).exists():
            shutil.rmtree(Path(_get_tui_docdir(mode)))
        Path(_get_tui_docdir(mode)).mkdir(exist_ok=True)
        index_file = Path(_get_tui_docdir(mode)) / "index.rst"
        with open(index_file, "w", encoding="utf8") as f:
            f.write(f".. _ref_{mode}_tui:\n\n")
            heading = mode + ".tui"
            f.write(f"{heading}\n")
            f.write(f"{'=' * len(heading)}\n\n")
            f.write(
                f".. autoclass:: ansys.fluent.core.{mode}.{_get_tui_file_name(mode)}.main_menu\n"
            )
            f.write("   :members:\n")
            f.write("   :show-inheritance:\n")
            f.write("   :undoc-members:\n")
            f.write("   :autosummary:\n")
            f.write("   :autosummary-members:\n")


if __name__ == "__main__":
    generate()
