"""Provides a module for generating Fluent TUI .rst files."""

import fnmatch
import importlib
import os
import pathlib
from pathlib import Path
import re
from typing import Optional

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_attribute_classes(menu):
    """Get attribute classes.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod

    Returns
    -------
    attribute_classes: list
        Attributes of ``menu``.
    """
    attribute_classes = []
    attributes_dict = dict(vars(menu))
    for attr_name, attr_value in attributes_dict.items():
        if not attr_name.startswith("__"):
            attribute_classes.append(attributes_dict[attr_name])
    return attribute_classes


def _get_attribute_classes_with_and_without_members(menu=None):
    """Get classes with and without sub members as attributes.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod

    Returns
    -------
    with_members: list
        Attributes of ``menu`` with sub ``menu``.
    without_members: list
        Attributes of ``menu`` without sub ``menu``.
    """
    with_members = []
    without_members = []
    menu_members = _get_attribute_classes(menu)
    for menu_member in menu_members:
        if _get_attribute_classes(menu_member):
            with_members.append(menu_member)
        else:
            without_members.append(menu_member)
    return with_members, without_members


def _set_with_without_members(with_member, Menus):
    """Set both with and without members as attributes to ``Menus`` class.

    Parameters
    ----------
    with_member: type
        Attribute of ``menu`` with sub ``menu``.

    Returns
    -------
    with_members: list
        Attributes of ``menu`` with sub ``menu``.
    Menus: type
        ``Menus`` class.
    """
    with_members, without_members = _get_attribute_classes_with_and_without_members(
        with_member
    )
    setattr(
        Menus,
        with_member.__name__,
        dict(
            name=with_member, with_members=with_members, without_members=without_members
        ),
    )
    return with_members, Menus


def _get_attribute_classes_recursively(with_member, Menus):
    """Generate all attribute classes with and without members recursively.

    Parameters
    ----------
    with_member: type
        Attribute of ``menu`` with sub ``menu``.
    Menus: type
        ``Menus`` class.
    """
    with_members, Menus = _set_with_without_members(with_member, Menus)
    for with_member in with_members:
        _get_attribute_classes_recursively(with_member, Menus)


def _get_menu_name_path(menu):
    """Get menu name and path to generate .rst file and folder respectively.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod

    Returns
    -------
    full_name: str
        Full name of ``TUIMenu`` or ``TUIMethod``.
    full_path: str
        Full path of ``TUIMenu`` or ``TUIMethod``.
    """
    name_string = re.findall("ansys.*", str(menu))
    full_name = name_string[0][0:-2]
    path_string = re.findall("main_menu.*", full_name)
    path = path_string[0].lstrip("main_menu.")
    full_path = path.replace(".", "/")
    return full_name, full_path


def _get_tui_docdir(mode: str, path: Optional[str] = None):
    """Get tui doc directory to generate all .rst files.

    Parameters
    ----------
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    path: str
        Full path of ``TUIMenu`` or ``TUIMethod``.

    Returns
    -------
    doc_path: str
        TUI doc directory.
    """
    doc_path = pathlib.Path(os.path.normpath(os.path.join(_THIS_DIRNAME, "..")))
    return (
        doc_path / f"doc/source/api/{mode}/tui/{path}"
        if path
        else doc_path / f"doc/source/api/{mode}/tui"
    )


def _get_tui_file_path(mode: str):
    """Get tui_*.py file path.

    Parameters
    ----------
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.

    Returns
    -------
        TUI file path.
    """
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
    """Get tui_*.py file name.

    Parameters
    ----------
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.

    Returns
    -------
        TUI file name.
    """
    for file in os.listdir(_get_tui_file_path(mode)):
        if fnmatch.fnmatch(file, "tui_*.py"):
            return pathlib.Path(file).stem


def _get_sorted_members(members):
    """Sort members alphabetically.

    Parameters
    ----------
    members: list
        Attributes of ``TUIMenu`` or ``TUIMethod``.
    """
    return sorted([member.__name__ for member in members])


def _write_doc(menu, mode):
    """Write .rst file for each menu.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    """
    menu_name, menu_path = _get_menu_name_path(menu["name"])
    full_folder_path = _get_tui_docdir(mode, menu_path)
    Path(full_folder_path).mkdir(parents=True, exist_ok=True)
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


def _generate_all_attribute_classes(Menus, main_menu):
    """Set all attribute classes with and without members as attributes to ``Menus``
    class.

    Parameters
    ----------
    Menus: type
        ``Menus`` class.
    main_menu: type
        ``main_menu`` class.
    """
    with_members, without_members = _get_attribute_classes_with_and_without_members(
        main_menu
    )
    setattr(
        Menus,
        main_menu.__name__,
        dict(
            name=main_menu, with_members=with_members, without_members=without_members
        ),
    )
    for member in with_members:
        _get_attribute_classes_recursively(member, Menus)


def _generate_doc(Menus, mode):
    """Write .rst file for each attribute class.

    Parameters
    ----------
    Menus: type
        ``Menus`` class.
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    """
    all_menus_attrs = [attr for attr in dir(Menus) if not attr.startswith("__")]
    for attr in all_menus_attrs:
        menu_attr = getattr(Menus, attr)
        _write_doc(menu_attr, mode)


def generate(main_menu, mode):
    """Generate .rst files.

    Parameters
    ----------
    main_menu: type
        ``main_menu`` class.
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    """

    class Menus:
        """Sets all sub classes as attributes."""

        pass

    _generate_all_attribute_classes(Menus, main_menu)
    _generate_doc(Menus, mode)


if __name__ == "__main__":
    meshing_tui = importlib.import_module(
        f"ansys.fluent.core.meshing.{_get_tui_file_name('meshing')}"
    )
    generate(meshing_tui.main_menu, "meshing")
    solver_tui = importlib.import_module(
        f"ansys.fluent.core.solver.{_get_tui_file_name('solver')}"
    )
    generate(solver_tui.main_menu, "solver")
