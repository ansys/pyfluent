# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
