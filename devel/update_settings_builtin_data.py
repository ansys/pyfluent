"""
Script to update the settings_builtin_data.py file with the new Fluent version.
Usage: python devel/update_settings_builtin_data.py --version 252
"""

import argparse
from pathlib import Path

from ansys.fluent.core.utils.fluent_version import FluentVersion

parser = argparse.ArgumentParser()
parser.add_argument("--version", type=str, required=True)
args = parser.parse_args()
new_version = FluentVersion(args.version).name
index = FluentVersion._member_names_.index(new_version)
previous_version = FluentVersion._member_names_[index + 1]

file_path = (
    Path(__file__).parent.parent
    / "src"
    / "ansys"
    / "fluent"
    / "core"
    / "solver"
    / "settings_builtin_data.py"
).resolve()
lines = []

with open(file_path, "r") as file:
    for line in file:
        if previous_version in line:
            new_line = line.replace(previous_version, new_version)
            lines.append(new_line)
        lines.append(line)

with open(file_path, "w") as file:
    file.writelines(lines)
