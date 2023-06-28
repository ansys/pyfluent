"""Provide a module to generate the documentation classes for Fluent settings
tree.
Running this module generates a .rst files for the Fluent
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
    --- Use the filename of the child class to generate the hyperlink to that class.
    --- Use the __doc__ property to generate the short summary for the corresponding child
    --- Use the previously generated perents dict to populate the parents table.
Usage
-----
python <path to settings_rstgen.py>
"""

import importlib
import os

from ansys.fluent.core.utils.fluent_version import get_version_for_filepath

parents_dict = {}
rst_list = []


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _generate_table_for_rst(r, data_dict={}):
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
            child_cls = getattr(cls, child)
            child_file = child_cls.__module__.split(".")[-1]
            if not parents_dict.get(child_file):
                parents_dict[child_file] = []
            if not cls in parents_dict[child_file]:
                parents_dict[child_file].append(cls)

    if hasattr(cls, "command_names"):
        for child in cls.command_names:
            child_cls = getattr(cls, child)
            child_file = child_cls.__module__.split(".")[-1]
            if not parents_dict.get(child_file):
                parents_dict[child_file] = []
            if not cls in parents_dict[child_file]:
                parents_dict[child_file].append(cls)

    if hasattr(cls, "argument_names"):
        for child in cls.argument_names:
            child_cls = getattr(cls, child)
            child_file = child_cls.__module__.split(".")[-1]
            if not parents_dict.get(child_file):
                parents_dict[child_file] = []
            if not cls in parents_dict[child_file]:
                parents_dict[child_file].append(cls)

    if hasattr(cls, "child_object_type"):
        child_cls = getattr(cls, "child_object_type")
        child_file = child_cls.__module__.split(".")[-1]
        if not parents_dict.get(child_file):
            parents_dict[child_file] = []
        if not cls in parents_dict[child_file]:
            parents_dict[child_file].append(cls)

    if hasattr(cls, "child_names"):
        for child in cls.child_names:
            _populate_parents_list(getattr(cls, child))

    if hasattr(cls, "command_names"):
        for child in cls.command_names:
            _populate_parents_list(getattr(cls, child))

    if hasattr(cls, "argument_names"):
        for child in cls.argument_names:
            _populate_parents_list(getattr(cls, child))

    if hasattr(cls, "child_object_type"):
        _populate_parents_list(getattr(cls, "child_object_type"))


def _populate_rst_from_settings(rst_dir, cls, version):
    istr1 = _get_indent_str(1)
    cls_name = cls.__name__
    file_name = cls.__module__.split(".")[-1]
    rstpath = os.path.normpath(os.path.join(rst_dir, file_name + ".rst"))
    has_children = hasattr(cls, "child_names") and len(cls.child_names) > 0
    has_commands = hasattr(cls, "command_names") and len(cls.command_names) > 0
    has_arguments = hasattr(cls, "argument_names") and len(cls.argument_names) > 0
    has_named_object = hasattr(cls, "child_object_type")
    with open(rstpath, "w") as r:
        # Populate initial rst
        r.write(":orphan:\n\n")
        r.write(f".. _{file_name}:\n\n")
        r.write(f"{cls_name}\n")
        r.write(f'{"="*(len(cls_name))}\n\n')
        r.write(
            f".. autoclass:: ansys.fluent.core.solver.settings_{version}.{file_name}.{cls_name}\n"
        )
        r.write(f"{istr1}:show-inheritance:\n\n")

        if has_children:
            r.write(f".. rubric:: Attributes\n\n")
            data_dict = {}
            data_dict["Attribute"] = "Summary"
            for child in cls.child_names:
                child_cls = getattr(cls, child)
                ref_string = f":ref:`{child} <{child_cls.__module__.split('.')[-1]}>`"
                data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

        if has_commands:
            r.write(f".. rubric:: Methods\n\n")
            data_dict = {}
            data_dict["Method"] = "Summary"
            for child in cls.command_names:
                child_cls = getattr(cls, child)
                ref_string = f":ref:`{child} <{child_cls.__module__.split('.')[-1]}>`"
                data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

        if has_arguments:
            r.write(f".. rubric:: Arguments\n\n")
            data_dict = {}
            data_dict["Argument"] = "Summary"
            for child in cls.argument_names:
                child_cls = getattr(cls, child)
                ref_string = f":ref:`{child} <{child_cls.__module__.split('.')[-1]}>`"
                data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

        if has_named_object:
            child_cls = getattr(cls, "child_object_type")
            ref_string = (
                f":ref:`{child_cls.__name__} <{child_cls.__module__.split('.')[-1]}>`"
            )
            data_dict = {}
            data_dict[ref_string] = child_cls.__doc__.strip("\n").split("\n")[0]
            r.write(f".. rubric:: Named object type\n\n")
            r.write(f"{ref_string}\n\n\n")

        if parents_dict.get(file_name):
            r.write(f".. rubric:: Included in:\n\n")
            data_dict = {}
            data_dict["Parent"] = "Summary"
            for parent in parents_dict.get(file_name):
                parent_file = parent.__module__.split(".")[-1]
                ref_string = f":ref:`{parent.__name__} <{parent_file}>`"
                data_dict[ref_string] = parent.__doc__.strip("\n").split("\n")[0]
            _generate_table_for_rst(r, data_dict)

    if not rstpath in rst_list:
        rst_list.append(rstpath)
        if has_children:
            for child in cls.child_names:
                _populate_rst_from_settings(rst_dir, getattr(cls, child), version)

        if has_commands:
            for child in cls.command_names:
                _populate_rst_from_settings(rst_dir, getattr(cls, child), version)

        if has_arguments:
            for child in cls.argument_names:
                _populate_rst_from_settings(rst_dir, getattr(cls, child), version)

        if has_named_object:
            _populate_rst_from_settings(
                rst_dir, getattr(cls, "child_object_type"), version
            )


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

    image_tag = os.getenv("FLUENT_IMAGE_TAG", "v23.2.0")
    version = get_version_for_filepath(image_tag.lstrip("v"))
    settings = importlib.import_module(f"ansys.fluent.core.solver.settings_{version}")
    _populate_parents_list(settings.root)
    _populate_rst_from_settings(rst_dir, settings.root, version)
