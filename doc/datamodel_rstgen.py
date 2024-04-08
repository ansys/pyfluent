"""Provides a module for generating the Fluent datamodel result files."""

"""Provides a module for generating Fluent TUI result files."""

import fnmatch
import os
from pathlib import Path

_THIS_DIRNAME = os.path.dirname(__file__)

# _THIS_DIRNAME - D:\pyfluent\doc
#
#
# _get_datamodel_folder_name - datamodel_242
#
#
# _get_datamodel_files - ['flicing.py', 'meshing.py', 'MeshingUtilities.py', 'PartManagement.py', 'PMFileManagement.py', 'preferences.py', 'solverworkflow.py', 'workflow.py']
#
# _get_datamodel_docdir - 'D:\\pyfluent\\doc\\source\\api\\meshing\\datamodel'


def _get_datamodel_docdir(mode: str):
    return os.path.normpath(
        os.path.join(
            _THIS_DIRNAME,
            "..",
            "doc",
            "source",
            "api",
            mode,
            "datamodel",
        )
    )


DATAMODEL_PATH = os.path.normpath(
    os.path.join(
        _THIS_DIRNAME,
        "..",
        "src",
        "ansys",
        "fluent",
        "core",
    )
)


def _get_datamodel_folder_name():
    for folder in os.listdir(DATAMODEL_PATH):
        if fnmatch.fnmatch(folder, "datamodel_*"):
            return folder


def _get_datamodel_files():
    files = []
    for file in os.listdir(Path(DATAMODEL_PATH) / _get_datamodel_folder_name()):
        files.append(file)
    return files


# def generate():
#     """Generates TUI .rst files."""
#     for mode in ["meshing", "solver"]:
#         if Path(_get_tui_docdir(mode)).exists():
#             shutil.rmtree(Path(_get_tui_docdir(mode)))
#         Path(_get_tui_docdir(mode)).mkdir(exist_ok=True)
#         index_file = Path(_get_tui_docdir(mode)) / "index.rst"
#         with open(index_file, "w", encoding="utf8") as f:
#             f.write(f".. _ref_{mode}_tui:\n\n")
#             heading = mode + ".tui"
#             f.write(f"{heading}\n")
#             f.write(f"{'=' * len(heading)}\n\n")
#             f.write(
#                 f".. autoclass:: ansys.fluent.core.{mode}.{_get_tui_file_name(mode)}.main_menu\n"
#             )
#             f.write("   :members:\n")
#             f.write("   :show-inheritance:\n")
#             f.write("   :undoc-members:\n")
#             f.write("   :autosummary:\n")
#             f.write("   :autosummary-members:\n")


if __name__ == "__main__":
    # generate()
    print(f"\n_THIS_DIRNAME - {_THIS_DIRNAME}\n")
    print(f"\n_get_datamodel_folder_name - {_get_datamodel_folder_name()}\n")
    print(f"\n_get_datamodel_files - {_get_datamodel_files()}\n")
