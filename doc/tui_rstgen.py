"""Provides a module for generating Fluent TUI result files."""

import fnmatch
import os
import pathlib
from pathlib import Path
import re
from typing import Optional

from ansys.fluent.core.solver.tui_242 import main_menu

_THIS_DIRNAME = os.path.dirname(__file__)


class all_menus:
    """all menus."""

    pass


def _get_menu_attribute_classes(menu):
    attribute_classes = []
    attributes_dict = dict(vars(menu))
    for attr_name, attr_value in attributes_dict.items():
        if not attr_name.startswith("__"):
            attribute_classes.append(attributes_dict[attr_name])
    return attribute_classes


def _get_attribute_classes_with_and_without_members(menu=None):
    with_members = []
    without_members = []
    menu_members = _get_menu_attribute_classes(menu)
    for menu_member in menu_members:
        if _get_menu_attribute_classes(menu_member):
            with_members.append(menu_member)
        else:
            without_members.append(menu_member)
    return with_members, without_members


with_members, without_members = _get_attribute_classes_with_and_without_members(
    main_menu
)

setattr(
    all_menus,
    main_menu.__name__,
    dict(name=main_menu, with_members=with_members, without_members=without_members),
)


def _set_with_without_members(wm):
    with_members, without_members = _get_attribute_classes_with_and_without_members(wm)
    setattr(
        all_menus,
        wm.__name__,
        dict(name=wm, with_members=with_members, without_members=without_members),
    )
    return with_members


def _recursive(wm):
    with_members = _set_with_without_members(wm)
    for wm in with_members:
        _recursive(wm)


def _get_menu_name_path(menu):
    name_string = re.findall("ansys.*", str(menu))
    full_name = name_string[0][0:-2]
    path_string = re.findall("main_menu.*", full_name)
    full_path = path_string[0].lstrip("main_menu.")
    return full_name, full_path


def _get_tui_docdir(mode: str, path: Optional[str] = None):
    doc_path = pathlib.Path(os.path.normpath(os.path.join(_THIS_DIRNAME, "..")))
    return (
        doc_path / f"doc/source/api/{mode}/tui/{path}"
        if path
        else doc_path / f"doc/source/api/{mode}/tui"
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


def _get_tui_file_name(mode: str, stem: bool):
    for file in os.listdir(_get_tui_filepath(mode)):
        if fnmatch.fnmatch(file, "tui_*.py"):
            if stem:
                return pathlib.Path(file).stem
            else:
                return file


def _get_sorted_members(members):
    return sorted([member.__name__ for member in members])


def _write_doc(menu, mode):
    menu_name, menu_path = _get_menu_name_path(menu["name"])
    full_folder_path = _get_tui_docdir(mode, menu_path)
    Path(full_folder_path).mkdir(exist_ok=True)
    index_file = Path(full_folder_path) / "index.rst"
    with open(index_file, "w", encoding="utf8") as f:
        f.write(f".. _ref_{mode}_tui_{menu['name'].__name__}:\n\n")
        f.write(f"{menu['name'].__name__}\n")
        f.write(f"{'=' * len(menu['name'].__name__)}\n\n")
        f.write(f".. autoclass:: {menu_name}\n")
        f.write(
            f"   :members: {', '.join(_get_sorted_members(menu['without_members']))}\n"
        )
        f.write("   :show-inheritance:\n")
        f.write("   :undoc-members:\n")
        f.write("   :autosummary:\n")
        f.write("   :autosummary-members:\n\n")

        if menu["with_members"]:
            f.write(".. toctree::\n")
            f.write("   :hidden:\n\n")
            for member in _get_sorted_members(menu["with_members"]):
                f.write(f"   {member}/index\n")


def _generate(main_menu):
    class all_menus:
        """all menus."""

        pass

    with_members, without_members = _get_attribute_classes_with_and_without_members(
        main_menu
    )

    setattr(
        all_menus,
        main_menu.__name__,
        dict(
            name=main_menu, with_members=with_members, without_members=without_members
        ),
    )

    Path(_get_tui_docdir("solver_test")).mkdir(exist_ok=True)
    for member in with_members[3:4]:
        _recursive(member)
        wm_attr = getattr(all_menus, member.__name__)
        _write_doc(wm_attr, "solver_test")


if __name__ == "__main__":
    from ansys.fluent.core.solver.tui_242 import main_menu

    _generate(main_menu)
