"""Module to generate Fluent API classes."""

from pathlib import Path
import pickle

from ansys.fluent.core import codegen
from ansys.fluent.core.codegen import (
    builtin_settingsgen,
    datamodelgen,
    settingsgen,
    tuigen,
)
from ansys.fluent.core.search import get_api_tree_file_name
from ansys.fluent.core.utils.fluent_version import FluentVersion


def _update_first_level(d, u):
    for k in d:
        d[k].update(u.get(k, {}))


def generate(version: str, static_infos: dict):
    """Generate Fluent API classes."""
    api_tree = {"<meshing_session>": {}, "<solver_session>": {}}
    _update_first_level(api_tree, tuigen.generate(version, static_infos))
    _update_first_level(api_tree, datamodelgen.generate(version, static_infos))
    _update_first_level(api_tree, settingsgen.generate(version, static_infos))
    api_tree_file = get_api_tree_file_name(version)
    Path(api_tree_file).parent.mkdir(parents=True, exist_ok=True)
    with open(api_tree_file, "wb") as f:
        pickle.dump(api_tree, f)
    if codegen.CODEGEN_GENERATE_BUILTIN_SETTINGS and FluentVersion(version) == next(
        iter(FluentVersion)
    ):
        builtin_settingsgen.generate(version)


if __name__ == "__main__":
    generate()
