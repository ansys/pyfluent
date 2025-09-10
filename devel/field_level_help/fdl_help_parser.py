"""FDL Help Text Inserter."""

import json
from pathlib import Path
import re


def get_indentation(line: str) -> str:
    """
    Returns the leading whitespace (indentation) from a given line using regex.
    """
    match = re.match(r"^\s*", line)
    return match.group(0) if match else ""


def insert_help_texts(fdl_path: Path, help_path: Path):
    """
    Inserts improved help texts into the FDL file based on the provided help dictionary.

    Args:
        fdl_path (Path): Path to the FDL file.
        help_path (Path): Path to the JSON file containing improved help texts.
    """

    with open(fdl_path, "r") as f:
        fdl_lines = f.readlines()

    with open(help_path, "r") as f:
        help_dict = json.load(f)

    new_fdl_lines = []
    commands = []
    singletons = []
    parent_field_map = {}

    for fdl_line in fdl_lines:
        if "COMMAND:" in fdl_line:
            command_name = fdl_line.split(":")[-1].strip()
            commands.append(command_name)
        elif "SINGLETON:" in fdl_line:
            singleton_name = fdl_line.split(":")[-1].strip()
            singletons.append(singleton_name)

    for fdl_line in fdl_lines:
        new_fdl_lines.append(fdl_line)
        for field, help_text in help_dict.items():
            field_parts = field.split(".")
            parent = field_parts[-2]
            field = field_parts[-1]
            improved_help = help_text[1]
            field_name = ""
            if "COMMAND:" in fdl_line:
                command_name = fdl_line.split(":")[-1].strip()
                commands.append(command_name)
            elif "SINGLETON:" in fdl_line:
                singleton_name = fdl_line.split(":")[-1].strip()
                singletons.append(singleton_name)
            elif any(
                field_type in fdl_line
                for field_type in ["STRING", "LOGICAL", "INTEGER", "REAL"]
            ):
                field_name = fdl_line.split(":")[1].strip()

            if field_name:
                if (
                    parent == commands[-1] or parent == singletons[-1]
                ) and field == field_name:
                    if field_name not in parent_field_map.get(
                        parent, set()
                    ):  # noqa: E713
                        index = fdl_lines.index(fdl_line)
                        indent = (
                            f"    {get_indentation(fdl_lines[index + 1])}"
                            if "END" == fdl_lines[index + 1].strip()
                            else get_indentation(fdl_lines[index + 1])
                        )
                        new_help_line = f'{indent}APIHelpText = "{improved_help}"\n'
                        if new_help_line not in new_fdl_lines:
                            new_fdl_lines.append(new_help_line)
                            parent_field_map[parent] = set()
                            parent_field_map[parent].add(field_name)

    with open(fdl_path, "w") as f:
        f.writelines(new_fdl_lines)


if __name__ == "__main__":
    fdl_paths = [Path(r"<file_path_1>"), Path(r"<file_path_2>")]

    help_path = Path(__file__).parents[0].resolve() / "improved_field_help_texts.json"
    for fdl_path in fdl_paths:
        insert_help_texts(fdl_path, help_path)
