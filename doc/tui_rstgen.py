"""Provides a module for generating Fluent TUI result files."""

import fnmatch
import os
import pathlib
from pathlib import Path
from typing import Optional

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_tui_docdir(mode: str, path: Optional[str] = None):
    doc_path = pathlib.Path(os.path.normpath(os.path.join(_THIS_DIRNAME, "..")))
    return (
        doc_path / f"doc/source/api/{mode}/{path}"
        if path
        else doc_path / f"doc/source/api/{mode}"
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


def _get_menu_name_path(menu):
    name_string = re.findall("ansys.*", str(menu))
    full_name = name_string[0][0:-2]
    path_string = re.findall("main_menu.*", full_name)
    full_path = path_string[0].lstrip("main_menu.")
    return full_name, full_path


def _dir_structure(main_menu):
    menus = {}
    with_members, without_members = _get_attribute_classes_with_and_without_members(
        main_menu
    )
    menus["main_menu"] = dict(
        with_members=with_members, without_members=without_members
    )
    for menu in menus["main_menu"]["with_members"]:
        with_members, without_members = _get_attribute_classes_with_and_without_members(
            menu
        )
        menus[menu.__name__] = dict(
            with_members=with_members, without_members=without_members
        )


def _write_doc(menu, mode):
    menu_name, menu_path = _get_menu_name_path(menu)
    full_folder_path = _get_tui_docdir(mode, menu_path)
    Path(full_folder_path).mkdir(exist_ok=True)
    index_file = Path(full_folder_path) / "index.rst"
    with open(index_file, "w", encoding="utf8") as f:
        f.write(f".. _ref_{mode}_tui_{menu.__name__}:\n\n")
        f.write(f"{menu.__name__}\n")
        f.write(f"{'=' * len(menu.__name__)}\n\n")
        f.write(f".. autoclass:: {menu_name}\n")
        f.write(f"   :members: {', '.join(menu_without_members)}\n")
        f.write("   :show-inheritance:\n")
        f.write("   :undoc-members:\n")
        f.write("   :autosummary:\n")
        f.write("   :autosummary-members:\n\n")

        if menu_with_members:
            f.write(".. toctree::\n")
            f.write("   :hidden:\n\n")
            for menu_member in menu_with_members:
                f.write(f"   {menu_member}/index\n")


if __name__ == "__main__":
    import re

    from ansys.fluent.core.solver.tui_242 import main_menu

    def _get_menu_attribute_classes(main_menu):
        attribute_classes = []
        for k, v in dict(vars(main_menu)).items():
            if not k.startswith("__"):
                attribute_classes.append(v)
        return sorted(attribute_classes)

    # def _get_members(class_name):
    #     return [member for member in dir(class_name) if not member.startswith("__")]

    def _get_attribute_classes_with_and_without_members(menu=None):
        attribute_classes_with_members = []
        attribute_classes_without_members = []
        menu_members = _get_menu_attribute_classes(menu)
        for menu_member in menu_members:
            if _get_menu_attribute_classes(menu_member):
                attribute_classes_with_members.append(menu_member)
            else:
                attribute_classes_without_members.append(menu_member)
        return attribute_classes_with_members, attribute_classes_without_members

    def _get_menu_name(menu):
        full_name = re.findall("ansys.*", str(menu))
        return full_name[0][0:-2]

    def _generate_main_menu_tui(main_menu, path, mode):
        folder_path = path
        Path(folder_path).mkdir(exist_ok=True)
        main_menu_index_file = Path(folder_path) / "index.rst"
        main_menu_with_members, main_menu_without_members = (
            _get_sub_menus_with_and_without_members(main_menu)
        )
        menu_attribute_classes = {}
        menu_vars = dict(vars(main_menu))
        with open(main_menu_index_file, "w", encoding="utf8") as f:
            f.write(f".. _ref_{mode}_tui:\n\n")
            f.write(f"{mode}.tui\n")
            f.write(f"{'=' * len(f'{mode}.tui')}\n\n")
            f.write(f".. autoclass:: {main_menu.__module__}.main_menu\n")
            f.write(f"   :members: {', '.join(main_menu_without_members)}\n")
            f.write("   :show-inheritance:\n")
            f.write("   :undoc-members:\n")
            f.write("   :autosummary:\n")
            f.write("   :autosummary-members:\n\n")
            f.write(".. toctree::\n")
            f.write("   :hidden:\n\n")
            for member in main_menu_with_members:
                f.write(f"   {member}/index\n")
                menu_attribute_classes[member] = menu_vars[member]
        return menu_attribute_classes

    def _generate_tui_recursively(menu_name, path, mode, menu):
        final_menu_with_members = {}
        Path(path).mkdir(exist_ok=True)
        index_file = Path(path) / "index.rst"
        menu_with_members, menu_without_members = (
            _get_sub_menus_with_and_without_members(menu)
        )
        if menu_with_members:
            final_menu_with_members[menu_name] = menu
        with open(index_file, "w", encoding="utf8") as f:
            f.write(f".. _ref_{mode}_tui_{menu_name}:\n\n")
            f.write(f"{menu_name}\n")
            f.write(f"{'=' * len(menu_name)}\n\n")
            f.write(f".. autoclass:: {_get_menu_name(menu)}\n")
            f.write(f"   :members: {', '.join(menu_without_members)}\n")
            f.write("   :show-inheritance:\n")
            f.write("   :undoc-members:\n")
            f.write("   :autosummary:\n")
            f.write("   :autosummary-members:\n\n")

            if menu_with_members:
                f.write(".. toctree::\n")
                f.write("   :hidden:\n\n")
                for menu_member in menu_with_members:
                    f.write(f"   {menu_member}/index\n")

        return final_menu_with_members

    menu_with_members = []

    menu_with_members = _generate_main_menu_tui(
        main_menu=main_menu, path=_get_tui_docdir("solver_test"), mode="solver"
    )

    print(f" \n menu_attribute_classes = {menu_with_members} \n")

    if menu_with_members:
        new_menu_with_members = {}
        for menu_name, menu in menu_with_members.items():
            new_menu_with_members.update(
                _generate_tui_recursively(
                    menu_name=menu_name,
                    path=_get_tui_docdir("solver_test", f"{menu_name}"),
                    mode="solver",
                    menu=menu,
                )
            )

        print(f" \n new_menu_with_members = {new_menu_with_members} \n")

    # mode = "solver"
    # Path(_get_tui_docdir("solver_test")).mkdir(exist_ok=True)
    #
    # main_menu_index_file = Path(_get_tui_docdir("solver_test")) / "index.rst"
    # menu_with_members, menu_without_members = _get_sub_menus_with_and_without_members(
    #     main_menu
    # )
    # with open(main_menu_index_file, "w", encoding="utf8") as f:
    #     f.write(f".. _ref_{mode}_tui:\n\n")
    #     f.write(f"{mode}.tui\n")
    #     f.write(f"{'=' * len(f'{mode}.tui')}\n\n")
    #     f.write(
    #         f".. autoclass:: ansys.fluent.core.solver.{_get_tui_file_name(mode, stem=True)}.main_menu\n"
    #     )
    #     main_menu_with_members, main_menu_without_members = (
    #         _get_sub_menus_with_and_without_members(main_menu)
    #     )
    #     f.write(f"   :members: {', '.join(main_menu_without_members)}\n")
    #     f.write("   :show-inheritance:\n")
    #     f.write("   :undoc-members:\n")
    #     f.write("   :autosummary:\n")
    #     f.write("   :autosummary-members:\n\n")
    #
    #     f.write(".. toctree::\n")
    #     f.write("   :hidden:\n\n")
    #     for member in main_menu_with_members:
    #         f.write(f"   {member}/index\n")
    #
    # for member in main_menu_with_members:
    #     Path(_get_tui_docdir("solver_test", member)).mkdir(exist_ok=True)
    #     index_file = Path(_get_tui_docdir("solver_test", member)) / "index.rst"
    #     with open(index_file, "w", encoding="utf8") as f:
    #         f.write(f".. _ref_{mode}_tui_{member}:\n\n")
    #         f.write(f"{member}\n")
    #         f.write(f"{'=' * len(member)}\n\n")
    #         f.write(
    #             f".. autoclass:: ansys.fluent.core.solver.{_get_tui_file_name(mode, stem=True)}.main_menu.{member}\n"
    #         )
    #         sub_menu = getattr(main_menu, member)
    #         menu_with_members, menu_without_members = (
    #             _get_sub_menus_with_and_without_members(main_menu, sub_menu)
    #         )
    #         f.write(f"   :members: {', '.join(menu_without_members)}\n")
    #         f.write("   :show-inheritance:\n")
    #         f.write("   :undoc-members:\n")
    #         f.write("   :autosummary:\n")
    #         f.write("   :autosummary-members:\n\n")
    #
    #         if menu_with_members:
    #             f.write(".. toctree::\n")
    #             f.write("   :hidden:\n\n")
    #             for menu_member in menu_with_members:
    #                 f.write(f"   {menu_member}/index\n")
    #
    #             for menu_member in menu_with_members:
    #                 Path(
    #                     Path(_get_tui_docdir("solver_test", member)) / menu_member
    #                 ).mkdir(exist_ok=True)
    #                 menu_member_index_file = (
    #                     Path(Path(_get_tui_docdir("solver_test", member)) / menu_member)
    #                     / "index.rst"
    #                 )
    #                 with open(menu_member_index_file, "w", encoding="utf8") as f:
    #                     f.write(f".. _ref_{mode}_tui_{member}_{menu_member}:\n\n")
    #                     f.write(f"{menu_member}\n")
    #                     f.write(f"{'=' * len(menu_member)}\n\n")
    #                     f.write(
    #                         f".. autoclass:: ansys.fluent.core.solver.{_get_tui_file_name(mode, stem=True)}.main_menu.{member}.{menu_member}\n"
    #                     )
    #                     sub_menu_member = getattr(sub_menu, menu_member)
    #                     menu_with_members, menu_without_members = (
    #                         _get_sub_menus_with_and_without_members(
    #                             sub_menu, sub_menu_member
    #                         )
    #                     )
    #                     f.write(f"   :members: {', '.join(menu_without_members)}\n")
    #                     f.write("   :show-inheritance:\n")
    #                     f.write("   :undoc-members:\n")
    #                     f.write("   :autosummary:\n")
    #                     f.write("   :autosummary-members:\n\n")
    #
    #                     if menu_with_members:
    #                         f.write(".. toctree::\n")
    #                         f.write("   :hidden:\n\n")
    #                         for menu_member in menu_with_members:
    #                             f.write(f"   {menu_member}/index\n")
