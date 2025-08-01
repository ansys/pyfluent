"""Provide a module to generate the documentation classes for Fluent settings tree.
Running this module generates a .rst files for the Fluent.

settings classes. The out is placed at:
- doc/source/api/solver/_autosummary/settings
Process
-------
    - From the settings API classes recursively generate the list of parents for the current class.
    -- Populate a parents dictionary with current class file name (not class name) as key and list of parents file names (not class names) as value.
    - Recursively Generate the rst files for classes starting with settings.root.
    -- Add target reference as the file name for the given class. This is used by other classes to generate hyperlinks
    -- Add properties like members, undoc-memebers, show-inheritence to the autoclass directive.
    -- Generate the tables of children, commands, arguments, and parents.
    --- Get access to the respective properties and members on the class with get_attr.
    --- Use the file name of the child class to generate the hyperlink to that class.
    --- Use the __doc__ property to generate the short summary for the corresponding child
    --- Use the previously generated perents dict to populate the parents table.
Usage
-----
python <path to settings_rstgen.py>
"""

from contextlib import redirect_stdout
import importlib
import io
import os
from pathlib import Path

from deprecated_pyfluent_apis import PYFLUENT_DEPRECATED_DATA

from ansys.fluent.core import config
from ansys.fluent.core.search import search
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

parents_dict = {}
rst_list = []
deprecated_class_version = {}


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _generate_table_for_rst(r, data_dict=None):
    if data_dict is None:
        data_dict = {}
    # Get dimensions for columns
    key_max = len(max(data_dict.keys(), key=len))
    val_max = len(max(data_dict.values(), key=len))
    col_gap = 3
    total = key_max + val_max + col_gap
    # Top border
    r.write(f'{"="*key_max}{" "*col_gap}{"="*val_max}\n\n')
    header = True
    for key, value in data_dict.items():
        if header:
            # Write header and border
            r.write(f'{key}{" "*(total-len(key)-len(value))}{value}\n\n')
            r.write(f'{"="*key_max}{" "*col_gap}{"="*val_max}\n')
            header = False
        else:
            # actual data
            r.write(f'{key}{" "*(total-len(key)-len(value))}{value}\n\n')
    # Bottom border
    r.write(f'{"="*key_max}{" "*col_gap}{"="*val_max}\n\n')


def _populate_parents_list(cls):
    if hasattr(cls, "child_names"):
        for child in cls.child_names:
            child_cls = cls._child_classes[child]
            child_cls_name = child_cls.__name__
            if not parents_dict.get(child_cls_name):
                parents_dict[child_cls_name] = []
            if cls not in parents_dict[child_cls_name]:
                parents_dict[child_cls_name].append(cls)

    if hasattr(cls, "command_names"):
        for child in cls.command_names:
            child_cls = cls._child_classes[child]
            child_cls_name = child_cls.__name__
            if not parents_dict.get(child_cls_name):
                parents_dict[child_cls_name] = []
            if cls not in parents_dict[child_cls_name]:
                parents_dict[child_cls_name].append(cls)

    if hasattr(cls, "argument_names"):
        for child in cls.argument_names:
            child_cls = cls._child_classes[child]
            child_cls_name = child_cls.__name__
            if not parents_dict.get(child_cls_name):
                parents_dict[child_cls_name] = []
            if cls not in parents_dict[child_cls_name]:
                parents_dict[child_cls_name].append(cls)

    if hasattr(cls, "child_object_type"):
        child_cls = getattr(cls, "child_object_type")
        child_cls_name = child_cls.__name__
        if not parents_dict.get(child_cls_name):
            parents_dict[child_cls_name] = []
        if cls not in parents_dict[child_cls_name]:
            parents_dict[child_cls_name].append(cls)

    if hasattr(cls, "child_names"):
        for child in cls.child_names:
            _populate_parents_list(cls._child_classes[child])

    if hasattr(cls, "command_names"):
        for child in cls.command_names:
            _populate_parents_list(cls._child_classes[child])

    if hasattr(cls, "argument_names"):
        for child in cls.argument_names:
            _populate_parents_list(cls._child_classes[child])

    if hasattr(cls, "child_object_type"):
        _populate_parents_list(getattr(cls, "child_object_type"))


def _write_common(initial_param, r, cls, attr):
    # TODO Add clarifying comments here
    data_dict = {initial_param: "Summary"}
    for child in getattr(cls, attr):
        child_cls = cls._child_classes[child]
        ref_string = f":ref:`{child} <{child_cls.__name__}>`"
        data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
    _generate_table_for_rst(r, data_dict)


def _populate_rst_from_settings(rst_dir, cls, version):
    istr1 = _get_indent_str(1)
    cls_name = cls.__name__
    cls_orig_name = cls._python_name
    rstpath = os.path.normpath(os.path.join(rst_dir, cls_name + ".rst"))
    has_children = hasattr(cls, "child_names") and len(cls.child_names) > 0
    has_commands = hasattr(cls, "command_names") and len(cls.command_names) > 0
    has_arguments = hasattr(cls, "argument_names") and len(cls.argument_names) > 0
    has_named_object = hasattr(cls, "child_object_type")
    with open(rstpath, "w") as r:
        # Populate initial rst
        r.write(":orphan:\n\n")
        # ``root`` used to create a hyperlink for settings API
        if cls_orig_name == "root":
            r.write(f".. _ref_{cls_name}:\n\n")
        else:
            r.write(f".. _{cls_name}:\n\n")
        r.write(f"{cls_orig_name}\n")
        r.write(f'{"="*(len(cls_orig_name))}\n\n')
        deprecated = getattr(cls, "_deprecated_version", None)
        if deprecated:
            pyfluent_fluent_version = FluentVersion(float(cls._deprecated_version))
            release_version = str(pyfluent_fluent_version)
            r.write(f".. deprecated:: {release_version}\n\n")
            deprecated_class_version.update({cls_name: release_version})
        r.write(
            f".. autoclass:: ansys.fluent.core.generated.solver.settings_{version}.{cls_name}\n"
        )
        r.write(f"{istr1}:show-inheritance:\n\n")

        if has_children:
            r.write(".. rubric:: Attributes\n\n")
            _write_common("Attribute", r, cls, "child_names")

        if has_commands:
            r.write(".. rubric:: Methods\n\n")
            _write_common("Method", r, cls, "command_names")

        if has_arguments:
            r.write(".. rubric:: Arguments\n\n")
            _write_common("Argument", r, cls, "argument_names")

        if has_named_object:
            child_cls = getattr(cls, "child_object_type")
            ref_string = f":ref:`{child_cls.__name__} <{child_cls.__name__}>`"
            r.write(".. rubric:: Named object type\n\n")
            r.write(f"{ref_string}\n\n\n")

        if parents_dict.get(cls_name):
            r.write(".. rubric:: Included in:\n\n")
            data_dict = {"Parent": "Summary"}
            for parent in parents_dict.get(cls_name):
                parent_ref = parent.__name__
                if parent_ref == "root":
                    parent_ref = "ref_root"
                ref_string = f":ref:`{parent.__name__} <{parent_ref}>`"
                data_dict[ref_string] = parent.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

    if rstpath not in rst_list:
        rst_list.append(rstpath)
        if has_children:
            for child in cls.child_names:
                _populate_rst_from_settings(rst_dir, cls._child_classes[child], version)

        if has_commands:
            for child in cls.command_names:
                _populate_rst_from_settings(rst_dir, cls._child_classes[child], version)

        if has_arguments:
            for child in cls.argument_names:
                _populate_rst_from_settings(rst_dir, cls._child_classes[child], version)

        if has_named_object:
            _populate_rst_from_settings(
                rst_dir, getattr(cls, "child_object_type"), version
            )


def _write_deprecated_rst_table(rst_dir, deprecated_class_version):
    deprecated_rst = (Path(rst_dir).parents[2] / "deprecated_apis.rst").resolve()
    if deprecated_rst.exists():
        deprecated_rst.unlink()
    else:
        deprecated_rst.touch()

    deprecated_data = []
    fluent_header = ["Target", "Deprecated"]
    pyflunet_header = ["Target", "Deprecated", "Alternatives"]
    name = "Deprecated APIs"
    pyfluent_name = "Deprecated PyFluent APIs"
    fluent_name = "Deprecated Ansys Fluent APIs"
    buffer = io.StringIO()

    for class_name, deprecated_version in deprecated_class_version.items():
        with redirect_stdout(buffer):
            search(class_name)
        output = buffer.getvalue()
        out = output.split("\n")
        settings = set(
            [
                setting
                for setting in out
                if "tui" not in setting and "meshing" not in setting
            ]
        )
        for setting in settings:
            if setting and setting.split(".")[-1].split(" ")[0] == class_name:
                setting = (
                    setting.replace("<solver_session>", "solver")
                    .replace("<", "")
                    .replace(">", "")
                )
                settings_with_ref = f":ref:`{setting} <{class_name}>`"
                deprecated_data.append((settings_with_ref, deprecated_version))

    with open(deprecated_rst, "w", encoding="utf-8") as f:
        f.write(":orphan:\n\n")
        f.write(f"{name}\n")
        f.write(f'{"="*(len(name))}\n\n')

        f.write(f"{pyfluent_name}\n")
        f.write(f'{"-"*(len(pyfluent_name))}\n\n')
        f.write(".. list-table:: Deprecated PyFluent APIs\n")
        f.write("   :header-rows: 1\n\n")
        f.write("   * - " + "\n     - ".join(pyflunet_header) + "\n")
        for row in PYFLUENT_DEPRECATED_DATA:
            f.write("   * - " + "\n     - ".join(row) + "\n")

        f.write(f"{fluent_name}\n")
        f.write(f'{"-"*(len(fluent_name))}\n\n')
        f.write(".. list-table:: Deprecated Ansys Fluent APIs\n")
        f.write("   :header-rows: 1\n\n")
        f.write("   * - " + "\n     - ".join(fluent_header) + "\n")
        sorted_data = sorted(deprecated_data, key=lambda x: len(x[0]))
        for row in sorted_data:
            f.write("   * - " + "\n     - ".join(row) + "\n")


if __name__ == "__main__":
    print("Generating rst files for settings API classes")
    dirname = os.path.dirname(__file__)
    rst_dir = os.path.normpath(
        os.path.join(
            dirname,
            "source",
            "api",
            "solver",
            "_autosummary",
            "settings",
        )
    )

    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    image_tag = config.fluent_image_tag
    version = get_version_for_file_name(image_tag.lstrip("v"))
    settings = importlib.import_module(
        f"ansys.fluent.core.generated.solver.settings_{version}"
    )
    _populate_parents_list(settings.root)
    _populate_rst_from_settings(rst_dir, settings.root, version)
    _write_deprecated_rst_table(rst_dir, deprecated_class_version)
