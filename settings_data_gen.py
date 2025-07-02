"""Settings API examples generator."""

import importlib
import json
from pathlib import Path
import re
import time
from typing import Any, Dict

from ansys.fluent.core.solver.flobject import (
    Boolean,
    BooleanList,
    Filename,
    FilenameList,
    Integer,
    IntegerList,
    Map,
    Real,
    RealList,
    RealNumerical,
    RealVector,
    String,
    StringList,
)


def get_python_type(class_obj) -> str:
    """Get the Python type for a given class object."""
    type_map = [
        ((RealNumerical, Real), "float"),
        ((String, Filename), "str"),
        ((Integer,), "int"),
        ((FilenameList, StringList), "list[str]"),
        ((Boolean,), "bool"),
        (
            (
                RealList,
                RealVector,
            ),
            "list[float]",
        ),
        ((IntegerList,), "list[int]"),
        ((BooleanList,), "list[bool]"),
        ((Map,), "dict[str, Any]"),
    ]

    for classes, py_type in type_map:
        if any(cls in class_obj.__mro__ for cls in classes):
            return py_type

    return "Any"


start_time = time.time()

with open(
    r"D:\Repos\pyfluent\src\ansys\fluent\core\generated\api_tree\api_objects.json", "r"
) as file:
    data = json.load(file)

objects = []
for example in data["api_objects"]:
    if "solver_session" in example:
        objects.append(example.replace("<solver_session>", "solver_session"))
    # else:
    #     objects.append(example.replace("<meshing_session>", "meshing_session"))

tui = []
for example in data["api_tui_objects"]:
    if "solver_session" in example:
        tui.append(example.replace("<solver_session>", "solver_session"))
    else:
        tui.append(example.replace("<meshing_session>", "meshing_session"))

api_data = []
api_data.extend(objects)
# api_data.extend(tui)

api_data.sort(key=lambda x: (len(x), x))

# print(len(api_data))

element_type = []
for item in api_data:
    if item.endswith("(Object)"):
        element_type.append(f"T:{item}")
    elif item.endswith("(Command)") or item.endswith("(Query)"):
        element_type.append(f"M:{item}")
    elif item.endswith("(Parameter)"):
        element_type.append(f"P:{item}")
    else:
        element_type.append(f"F:{item}")

element_type_paths = []
for item in element_type:
    item_split = item.split(" ")
    element_type_paths.append(item_split[0])

# print(len(element_type_paths))

module_name = "ansys.fluent.core.generated.solver.settings_261"  # Replace with your module name (without .py)
module = importlib.import_module(module_name)

pre_json_data = {}


def strip_parameters(docstring: str) -> str:
    """
    Strips everything from the 'Parameters' section onwards in the given docstring.

    Parameters
    ----------
    docstring: str
        The original docstring to process.

    Returns
    -------
        The modified docstring with the 'Parameters' section removed.
    """
    lines = docstring.strip().splitlines()
    filtered_lines = []

    for line in lines:
        if line.strip().startswith("Parameters"):
            break
        filtered_lines.append(line)

    return "\n".join(filtered_lines).strip()


def clean_parameter_names(parameters):
    """
    Cleans the parameter names by removing underscores and digits only if they appear at the end of each name.

    Parameters
    ----------
    parameters : dict
        A dictionary where keys are parameter names and values are their descriptions.

    Returns
    -------
    dict
        A new dictionary with cleaned parameter names.
    """
    cleaned_parameters = {}

    for param_name, description in parameters.items():
        # Use regex to remove '_<digit>' only if it appears at the end of the parameter name
        cleaned_name = re.sub(r"_\d$", "", param_name)
        cleaned_parameters[cleaned_name] = description

    return cleaned_parameters


def parse_docstring(docstring: str) -> Dict[str, Any]:
    """Parses the docstring to extract parameters and their types."""
    # Initialize an empty dictionary to hold the parsed parameters
    parameters = {}

    # Define a regex pattern to match parameter lines
    param_pattern = re.compile(r"^\s*(\w+)\s*:\s*(\w+)\s*\n\s+(.*)", re.MULTILINE)

    # Search for all matches in the docstring
    matches = param_pattern.findall(docstring)

    # Iterate over each match and populate the dictionary
    for match in matches:
        param_name = match[0]
        param_type = match[1]
        param_description = match[2].strip()

        parameters[param_name] = {"type": param_type, "description": param_description}

    return parameters


all_parameters = {}

for type_path in element_type_paths:
    if any(
        substring in type_path
        for substring in [".workflow.", ".solverworkflow.", ".preferences."]
    ):
        pass
    else:
        split = type_path.split(".")
        argument = split[-1]
        parent = split[-2]
        pre_json_data[type_path] = {}
        try:
            if parent[2:] == "solver_session":
                parent_obj = getattr(module, argument)
            else:
                try:
                    parent_obj = getattr(module, parent)
                except Exception:
                    parent_obj = getattr(module, argument)
            if hasattr(parent_obj, "_child_classes"):
                child_classes = getattr(parent_obj, "_child_classes")
                if child_classes and argument in child_classes:
                    class_obj = getattr(module, child_classes.get(argument).__name__)
                else:
                    class_obj = getattr(module, argument)
            else:
                class_obj = getattr(module, argument)

            pre_json_data[type_path]["docstring"] = strip_parameters(class_obj.__doc__)
            parameter_data = {}
            if not bool(parameter_data) and hasattr(class_obj, "argument_names"):
                args = getattr(class_obj, "argument_names")
                for arg in args:
                    arg_obj = getattr(class_obj, "_child_classes").get(arg)
                    parameter_data[arg] = {
                        "type": get_python_type(arg_obj),
                        "description": strip_parameters(arg_obj.__doc__),
                    }

            all_parameters.update(parameter_data)
            pre_json_data[type_path]["parameters"] = parameter_data
            pre_json_data[type_path]["examples"] = type_path.split(":")[1]
            pre_json_data[type_path]["type"] = get_python_type(class_obj)
        except AttributeError:
            pre_json_data[type_path]["docstring"] = ""
            pre_json_data[type_path]["parameters"] = {}
            pre_json_data[type_path]["examples"] = type_path.split(":")[1]
            pre_json_data[type_path]["type"] = "Any"

json_data = []

SETTINGS_EXAMPLES = []

for key, value in pre_json_data.items():
    data = {}
    argument_type = ""
    for parameter, info in value.get("parameters").items():
        if argument_type == "":
            argument_type += f"{parameter}: {info.get('type').lower()}"
        else:
            argument_type += f", {parameter}: {info.get('type').lower()}"
    if key.startswith("P:") or key.startswith("T:"):
        data["name"] = key
    else:
        data["name"] = f"{key}({argument_type})"

    example_data = {}
    if value.get("examples"):
        example = data["name"][2:].replace("solver_session", "solver")
        example += (
            f" = {value.get('type', 'Any')}" if data["name"].startswith("P:") else ""
        )
        if key.startswith("M:") or key.startswith("P:"):
            SETTINGS_EXAMPLES.append(example)
    json_data.append(data)

deprecated_rst = Path(
    r"D:\Repos\pyfluent\doc\source\user_guide\solver_settings\settings_examples.rst"
)
if deprecated_rst.exists():
    deprecated_rst.unlink()
else:
    deprecated_rst.touch()

name = "Settings API usage"

with open(deprecated_rst, "w", encoding="utf-8") as f:
    f.write(":orphan:\n\n")
    f.write(f"{name}\n")
    f.write(f'{"="*(len(name))}\n\n')
    f.write(".. list-table:: Settings API usage\n")
    f.write("   :header-rows: 1\n\n")
    sorted_examples = sorted(SETTINGS_EXAMPLES)
    for example in sorted_examples:
        f.write(f"   * - ``{example}``\n")

print("finished.")

end_time = time.time()

# Calculate elapsed time in seconds
elapsed_time_seconds = end_time - start_time

# Convert elapsed time to minutes
elapsed_time_minutes = elapsed_time_seconds / 60

print("Elapsed time: {:.2f} minutes".format(elapsed_time_minutes))
