"""Miscellaneous utility functions."""

import os
import re


def expand_api_file_argument(command_name, value, kwargs):
    """Expand API file argument."""
    if kwargs.get("file_type") == "case-data" or command_name in [
        "read_case_data",
        "write_case_data",
    ]:
        data_file = value.replace(".cas", ".dat")
        return [value, data_file]
    else:
        return [value]


def use_search(codegen_outdir: str, version: str):
    """Whether to use ``_search()`` in the error handling.

    Parameters
    ----------
    codegen_outdir: str
        Codegen directory.
    version: str
        Fluent version.
    """
    fluent_version_str = version
    fluent_version_int = int(fluent_version_str.replace(".", "")[0:3])
    api_tree_files = [
        file for file in os.listdir(codegen_outdir) if file.endswith("pickle")
    ]
    api_tree_file_versions = [
        int(re.findall(r"\d+", file)[0]) for file in api_tree_files
    ]
    latest_api_tree_version = max(api_tree_file_versions)
    if len(api_tree_files) == 1 and fluent_version_int == latest_api_tree_version:
        return True
    else:
        return False
