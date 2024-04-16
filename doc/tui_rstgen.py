"""Provides a module for generating Fluent TUI result files."""

import fnmatch
import os
from pathlib import Path
import shutil
from typing import Optional

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_tui_docdir(mode: str, member: Optional[str] = None):
    return (
        os.path.normpath(
            os.path.join(_THIS_DIRNAME, "..", "doc", "source", "api", mode, f"{member}")
        )
        if member
        else os.path.normpath(
            os.path.join(
                _THIS_DIRNAME,
                "..",
                "doc",
                "source",
                "api",
                mode,
            )
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
    """Generate TUI result (RST) files."""
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
    from ansys.fluent.core.solver.tui_242 import main_menu

    def _create_dir():
        return

    def _get_members(class_name):
        return [member for member in dir(class_name) if not member.startswith("__")]

    def _get_sub_menus_with_and_without_members(main_menu=None, sub_menu=None):
        menu_with_members = []
        menu_without_members = []
        if main_menu and sub_menu:
            sub_menu = getattr(main_menu, sub_menu.__name__)
            sub_menu_members = _get_members(sub_menu)
            for sub_menu_member in sub_menu_members:
                sub_sub_menu = getattr(sub_menu, sub_menu_member)
                if _get_members(sub_sub_menu):
                    menu_with_members.append(sub_sub_menu.__name__)
                else:
                    menu_without_members.append(sub_sub_menu.__name__)
        elif main_menu and not sub_menu:
            main_menu_members = _get_members(main_menu)
            for main_menu_member in main_menu_members:
                sub_main_menu = getattr(main_menu, main_menu_member)
                if _get_members(sub_main_menu):
                    menu_with_members.append(sub_main_menu.__name__)
                else:
                    menu_without_members.append(sub_main_menu.__name__)
        return menu_with_members, menu_without_members

    main_menu_members = _get_members(main_menu)
    mode = "solver"
    Path(_get_tui_docdir("solver_test")).mkdir(exist_ok=True)

    main_menu_index_file = Path(_get_tui_docdir("solver_test")) / "index.rst"
    menu_with_members, menu_without_members = _get_sub_menus_with_and_without_members(
        main_menu
    )
    with open(main_menu_index_file, "w", encoding="utf8") as f:
        f.write(f".. _ref_{mode}_tui:\n\n")
        f.write(f"{mode}.tui\n")
        f.write(f"{'=' * len(f'{mode}.tui')}\n\n")
        f.write(
            f".. autoclass:: ansys.fluent.core.solver.{_get_tui_file_name(mode)}.main_menu\n"
        )
        main_menu_with_members, main_menu_without_members = (
            _get_sub_menus_with_and_without_members(main_menu)
        )
        f.write(f"   :members: {', '.join(main_menu_without_members)}\n")
        f.write("   :show-inheritance:\n")
        f.write("   :undoc-members:\n")
        f.write("   :autosummary:\n")
        f.write("   :autosummary-members:\n\n")

        f.write(".. toctree::\n")
        f.write("   :hidden:\n\n")
        for member in main_menu_with_members:
            f.write(f"   {member}/index\n")

    for member in main_menu_members:
        Path(_get_tui_docdir("solver_test", member)).mkdir(exist_ok=True)
        index_file = Path(_get_tui_docdir("solver_test", member)) / "index.rst"
        with open(index_file, "w", encoding="utf8") as f:
            f.write(f".. _ref_{mode}_tui_{member}:\n\n")
            f.write(f"{member}\n")
            f.write(f"{'=' * len(member)}\n\n")
            f.write(
                f".. autoclass:: ansys.fluent.core.solver.{_get_tui_file_name(mode)}.main_menu.{member}\n"
            )
            sub_menu = getattr(main_menu, member)
            menu_with_members, menu_without_members = (
                _get_sub_menus_with_and_without_members(main_menu, sub_menu)
            )
            f.write(f"   :members: {', '.join(menu_without_members)}\n")
            f.write("   :show-inheritance:\n")
            f.write("   :undoc-members:\n")
            f.write("   :autosummary:\n")
            f.write("   :autosummary-members:\n\n")

            if menu_with_members:
                f.write(".. toctree::\n")
                f.write("   :hidden:\n\n")
                for member in menu_with_members:
                    f.write(f"   {member}/index\n")
