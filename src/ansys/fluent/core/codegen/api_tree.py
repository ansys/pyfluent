# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Api tree hierarchy."""
from collections.abc import Mapping
import json
import os
from pathlib import Path
import pickle

from ansys.fluent.core.module_config import config
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)


def get_api_tree_file_name(version: str) -> Path:
    """Get API tree file name."""
    return (config.codegen_outdir / f"api_tree_{version}.pickle").resolve()


def get_api_tree_data_file_path():
    """Get API tree data file."""
    return (config.codegen_outdir / "api_tree" / "api_objects.json").resolve()


def _remove_suffix(input: str, suffix):
    if hasattr(input, "removesuffix"):
        return input.removesuffix(suffix)
    else:
        if suffix and input.endswith(suffix):
            return input[: -len(suffix)]
        return input


def generate_api_data(
    version: str | None = None,
):
    """Generate API tree data.

    Parameters
    ----------
    version : str, optional
        Fluent version to search in. The default is ``None``. If ``None``,
        it searches in the latest version for which codegen was run.
    write_api_tree_data: bool, optional
        Whether to write the API tree data.
    """
    api_objects = set()
    api_tui_objects = set()
    api_object_name_map = {"meshing_session": set(), "solver_session": set()}
    api_object_names = set()
    if version:
        version = get_version_for_file_name(version)
    if not version:
        for fluent_version in FluentVersion:
            version = get_version_for_file_name(fluent_version.value)
            if get_api_tree_file_name(version).exists():
                break
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        # Safe to load: file is generated internally by PyFluent
        api_tree = pickle.load(f)  # nosec B301

    def inner(tree, path):
        for k, v in tree.items():
            if k in ("<meshing_session>", "<solver_session>"):
                next_path = k
            else:
                if k.endswith(":<name>"):
                    k = _remove_suffix(k, ":<name>")
                    next_path = f'{path}.{k}["<name>"]'
                elif k.endswith(":<index>"):
                    k = _remove_suffix(k, ":<index>")
                    next_path = f"{path}.{k}[<index>]"
                else:
                    next_path = f"{path}.{k}"
                type_ = "Object" if isinstance(v, Mapping) else v
                api_object_names.add(k)
                if "meshing_session" in next_path:
                    api_object_name_map["meshing_session"].add(k)
                if "solver_session" in next_path:
                    api_object_name_map["solver_session"].add(k)
                next_path = (
                    next_path.replace("MeshingUtilities", "meshing_utilities")
                    if "MeshingUtilities" in next_path
                    else next_path
                )
                if "tui" in next_path:
                    api_tui_objects.add(f"{next_path} ({type_})")
                else:
                    api_objects.add(f"{next_path} ({type_})")
            if isinstance(v, Mapping):
                inner(v, next_path)

    inner(api_tree, "")

    api_tree_data = dict()
    api_tree_data["api_objects"] = sorted(list(api_objects))
    api_tree_data["api_tui_objects"] = sorted(list(api_tui_objects))
    api_tree_data["all_api_object_names"] = sorted(list(api_object_names))
    api_object_name_map["meshing_session"] = sorted(
        list(api_object_name_map["meshing_session"])
    )
    api_object_name_map["solver_session"] = sorted(
        list(api_object_name_map["solver_session"])
    )
    api_tree_data["api_object_name_map"] = api_object_name_map

    def _write_api_tree_file(api_tree_data: dict, api_object_names: list):
        json_file_folder = Path(os.path.join(config.codegen_outdir, "api_tree"))
        json_file_folder.mkdir(parents=True, exist_ok=True)

        api_tree_file_path = get_api_tree_data_file_path()
        api_tree_file_path.touch()
        with open(api_tree_file_path, "w") as json_file:
            json.dump(api_tree_data, json_file)

    _write_api_tree_file(
        api_tree_data=api_tree_data, api_object_names=list(api_object_names)
    )

    api_tree_file.unlink()
