"""Provides a module for generating Fluent Datamodel and TUI RST files."""

import fnmatch
import os
import pathlib
from pathlib import Path
import re

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_attribute_classes(menu: type):
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


def _get_attribute_classes_with_and_without_members(menu: type):
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


def _add_with_without_members(with_member: type, all_menus: list):
    """Add both with and without members to ``all_menus`` list.

    Parameters
    ----------
    with_member: type
        Attribute of ``menu`` with sub ``menu``.
    all_menus: list
        ``all_menus`` list.

    Returns
    -------
    with_members: list
        Attributes of ``menu`` with sub ``menu``.
    all_menus: list
        ``all_menus`` list.
    """
    with_members, without_members = _get_attribute_classes_with_and_without_members(
        with_member
    )
    all_menus.append(
        dict(
            name=with_member, with_members=with_members, without_members=without_members
        )
    )
    return with_members, all_menus


def _get_attribute_classes_recursively(with_member: type, all_menus: list):
    """Generate all attribute classes with and without members recursively.

    Parameters
    ----------
    with_member: type
        Attribute of ``menu`` with sub ``menu``.
    all_menus: list
        ``all_menus`` list.
    """
    with_members, all_menus = _add_with_without_members(with_member, all_menus)
    for with_member in with_members:
        _get_attribute_classes_recursively(with_member, all_menus)


def _process_datamodel_path(full_name: str):
    """Get path for datamodel files.

    Parameters
    ----------
    full_name: str
        Full name of class.

    Returns:
    path: str
        Path of datamodel class.
    """
    path_string = re.findall("core.*", full_name)
    path = path_string[0].replace("core.generated.", "")
    path = re.sub("[0-9]", "", path)
    path = path.replace("Root." if "Root." in path else "Root", "")
    path = path.replace("datamodel_.", "")
    path = path.rstrip(".")
    path = path.replace(".", "/")
    return path


def _process_tui_path(full_name: str):
    """Get path for tui files.

    Parameters
    ----------
    full_name: str
        Full name of class.

    Returns:
    path: str
        Path of tui class.
    """
    path_string = re.findall("main_menu.*", full_name)
    path = path_string[0].replace("main_menu", "")
    path = path.lstrip(".")
    path = path.replace(".", "/")
    return path


def _get_menu_name_path(menu: type, is_datamodel: bool):
    """Get menu name and path to generate RST file and folder respectively.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod
    is_datamodel: bool
        Whether to select datamodel menu.

    Returns
    -------
    full_name: str
        Full name of ``TUIMenu`` or ``TUIMethod``.
    full_path: str
        Full path of ``TUIMenu`` or ``TUIMethod``.
    """
    name_string = re.findall("ansys.*", str(menu))
    full_name = name_string[0][0:-2]
    if is_datamodel:
        full_path = _process_datamodel_path(full_name)
    else:
        full_path = _process_tui_path(full_name)
    return full_name, full_path


def _get_docdir(mode: str, path: str | None = None, is_datamodel: bool | None = None):
    """Get tui doc directory to generate all RST files.

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
    if is_datamodel:
        return doc_path / f"doc/source/api/{mode}/datamodel/{path}"
    else:
        return doc_path / f"doc/source/api/{mode}/tui/{path}"


def _get_path(mode: str, is_datamodel: bool | None = None):
    """Get datamodel_* or tui_*.py file path.

    Parameters
    ----------
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    is_datamodel: bool
        Whether to get datamodel path.

    Returns
    -------
        Datamodel or TUI path.
    """
    if is_datamodel:
        return os.path.normpath(
            os.path.join(
                _THIS_DIRNAME,
                "..",
                "src",
                "ansys",
                "fluent",
                "core",
                "generated",
            )
        )
    else:
        return os.path.normpath(
            os.path.join(
                _THIS_DIRNAME,
                "..",
                "src",
                "ansys",
                "fluent",
                "core",
                "generated",
                f"{mode}",
            )
        )


def _get_file_or_folder(mode: str, is_datamodel: bool):
    """Get datamodel_* folder or tui_*.py file name.

    Parameters
    ----------
    mode: str
        Fluent session mode. Options are ``meshing`` and ``solver``.
    is_datamodel: bool
        Whether to get datamodel folder.

    Returns
    -------
        Datamodel or TUI file name.
    """
    for file in os.listdir(_get_path(mode, is_datamodel)):
        if is_datamodel and fnmatch.fnmatch(file, "datamodel_*"):
            return pathlib.Path(file).stem
        if not is_datamodel and fnmatch.fnmatch(file, "tui_*.py"):
            return pathlib.Path(file).stem


def _get_sorted_members(members: list):
    """Sort members alphabetically.

    Parameters
    ----------
    members: list
        Attributes of ``TUIMenu`` or ``TUIMethod``.
    """
    return sorted([member.__name__ for member in members])


def _write_datamodel_index_doc(datamodels: list, mode: str):
    """Write RST file for each datamodel.

    Parameters
    ----------
    datamodels: list
        Meshing and Solver datamodels.
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    """
    full_folder_path = _get_docdir(mode, "", True)
    Path(full_folder_path).mkdir(parents=True, exist_ok=True)
    index_file = Path(full_folder_path) / "index.rst"
    datamodel_mode = f"{mode}.datamodel"
    with open(index_file, "w", encoding="utf8") as f:
        f.write(f".. _ref_{mode}_datamodel:\n\n")
        f.write(f"{datamodel_mode}\n")
        f.write(f"{'=' * len(datamodel_mode)}\n\n")
        f.write(".. automodule:: ansys.fluent.core.datamodel\n")
        f.write("   :autosummary:\n\n")
        f.write("   :autosummary-members:\n\n")
        f.write(".. toctree::\n")
        f.write("   :hidden:\n\n")
        for datamodel in datamodels:
            f.write(f"   {datamodel}/index\n")


def _get_reference(menu: type, menu_path: str, mode: str, is_datamodel: bool):
    """Get reference for RST file.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod
    menu_path: str
        Menu folder path.
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    is_datamodel: bool
        Whether the menu is of datamodel.
    """
    if is_datamodel:
        if menu["name"].__name__ == "Root":
            reference = f".. _ref_{mode}_datamodel_{menu_path}:\n\n"
        else:
            reference = f".. _ref_{mode}_datamodel_{menu_path.rstrip('/').replace('/', '_')}:\n\n"
    else:
        if menu["name"].__name__ == "main_menu":
            reference = f".. _ref_{mode}_tui:\n\n"
        else:
            reference = f".. _ref_{mode}_tui_{menu_path.replace('/', '_')}:\n\n"
    return reference


def _get_title(mode: str, menu_path: str, menu: type, is_datamodel: bool):
    """Get title for RST.

    Parameters
    ----------
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    menu_path: str
        Menu folder path.
    menu: type
        TUIMenu, TUIMethod
    is_datamodel: bool
        Whether the menu is of datamodel.
    """
    if is_datamodel:
        title = (
            f"{mode}.datamodel.{menu_path}"
            if menu["name"].__name__ == "Root"
            else menu["name"].__name__
        )
    else:
        title = (
            f"{mode}.tui"
            if menu["name"].__name__ == "main_menu"
            else menu["name"].__name__
        )
    return title


def _write_doc(menu: type, mode: str, is_datamodel: bool):
    """Write RST file for each menu.

    Parameters
    ----------
    menu: type
        TUIMenu, TUIMethod
    mode: str
        Fluent session mode either ``meshing`` or ``solver``.
    is_datamodel: bool
        Whether to generate datamodel RST files.
    """
    menu_name, menu_path = _get_menu_name_path(menu["name"], is_datamodel)
    full_folder_path = _get_docdir(mode, menu_path, is_datamodel)
    Path(full_folder_path).mkdir(parents=True, exist_ok=True)
    index_file = Path(full_folder_path) / "index.rst"
    title = _get_title(mode, menu_path, menu, is_datamodel)
    with open(index_file, "w", encoding="utf8") as f:
        f.write(_get_reference(menu, menu_path, mode, is_datamodel))
        f.write(f"{title}\n")
        f.write(f"{'=' * len(title)}\n\n")
        f.write(f".. autoclass:: {menu_name}\n")
        f.write(
            f"   :members: {', '.join(_get_sorted_members(menu['without_members']))}\n"
        )
        f.write("   :show-inheritance:\n")
        f.write("   :undoc-members:\n")
        f.write("   :exclude-members: __weakref__, __dict__\n")
        f.write("   :special-members: __init__\n")
        f.write("   :autosummary:\n")
        f.write("   :autosummary-members:\n\n")

        if menu["with_members"]:
            f.write(".. toctree::\n")
            f.write("   :hidden:\n\n")
            for member in _get_sorted_members(menu["with_members"]):
                f.write(f"   {member}/index\n")


def _generate_all_attribute_classes(all_menus: list, main_menu: type):
    """Store all attribute classes with and without members into ``all_menus`` list.

    Parameters
    ----------
    all_menus: list
        ``all_menus`` list.
    main_menu: type
        ``main_menu`` or ``Root`` class.
    """
    with_members, without_members = _get_attribute_classes_with_and_without_members(
        main_menu
    )
    all_menus.append(
        dict(name=main_menu, with_members=with_members, without_members=without_members)
    )
    for member in with_members:
        _get_attribute_classes_recursively(member, all_menus)


def _generate_doc(all_menus: list, mode: str, is_datamodel: bool):
    """Write RST file for each attribute class.

    Parameters
    ----------
    all_menus: list
        ``all_menus`` list.
    mode: str
        Fluent session mode. Options are ``meshing`` and ``solver``.
    is_datamodel: bool
        Whether to generate datamodel RST files.
    """
    for menu in all_menus:
        _write_doc(menu, mode, is_datamodel)


def generate(main_menu: type, mode: str, is_datamodel: bool):
    """Generate RST files.

    Parameters
    ----------
    main_menu: type
        ``main_menu`` or ``Root`` class.
    mode: str
        Fluent session mode. Options are ``meshing`` and ``solver``.
    is_datamodel: bool
        Whether to generate datamodel RST files.
    """

    all_menus = []
    _generate_all_attribute_classes(all_menus, main_menu)
    _generate_doc(all_menus, mode, is_datamodel)
