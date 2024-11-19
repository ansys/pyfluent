"""Utility to write YAML file for the current settings hierarchy.

Usage:
     write_settings_yaml.py [outfile]
"""

import sys

import ansys.fluent.core as pyfluent

indent_factor = 2


def write_yaml(out, obj, indent=0):
    """Write a yaml file."""
    type = obj["type"]
    out.write(f"{' '*indent*indent_factor}type: {type}\n")
    for ctype in ["children", "commands", "arguments"]:
        children = obj.get(ctype)
        if children:
            out.write(f"{' '*indent*indent_factor}{ctype}:\n")
            for child, cobj in children.items():
                out.write(f"{' '*(indent+1)*indent_factor}{child}:\n")
                write_yaml(out, cobj, indent + 2)
    cobj = obj.get("object-type")
    if cobj:
        out.write(f"{' '*indent*indent_factor}child-object-type:\n")
        write_yaml(out, cobj, indent + 1)
    help_ = obj.get("help")
    if help_:
        out.write(f"{' '*indent*indent_factor}help: {help_}\n")


if "__main__" == __name__:
    if len(sys.argv) > 2:
        print("Usage: write_settings_yaml.py [outfile]")
    else:
        session = pyfluent.launch_fluent(mode="solver")
        static_info = session.settings_service.get_static_info()
        if len(sys.argv) == 2:
            with open(sys.argv[1], "w") as f:
                write_yaml(f, static_info)
        elif len(sys.argv) == 1:
            write_yaml(sys.stdout, static_info)
