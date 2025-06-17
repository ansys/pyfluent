"""
Script to update the settings_builtin_data.py file with the new Fluent version.
Usage: python devel/update_settings_builtin_data.py --version 252
"""

from pathlib import Path

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
    skip = False
    versions = []
    path = ""
    for line in file:
        if line.strip() == "{":
            skip = True
            lines.append(line)
            continue
        if line.strip() == "},":
            min_version = versions[-1]
            lines.append(f"            since({min_version}): {path}\n")
            skip = False
            versions = []
            path = ""
        if skip:
            version, path_ = line.strip().split(":", 1)
            if path:
                assert path == path_, line
            path = path_
            versions.append(version.strip())
        else:
            lines.append(line)

with open(file_path, "w") as file:
    file.writelines(lines)
