"""Module to generate Fluent API classes."""

import argparse
import os
from pathlib import Path
import pickle
import shutil

from ansys.fluent.core import GENERATED_API_DIR, FluentMode, launch_fluent
from ansys.fluent.core.codegen import (
    datamodelgen,
    print_fluent_version,
    settingsgen,
    tuigen,
)
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)
from ansys.fluent.core.utils.search import get_api_tree_file_name


def _update_first_level(d, u):
    for k in d:
        d[k].update(u.get(k, {}))


def generate():
    """Generate Fluent API classes."""
    api_tree = {"<meshing_session>": {}, "<solver_session>": {}}
    parser = argparse.ArgumentParser(
        description="Generate python code from Fluent APIs"
    )
    if not os.getenv("PYFLUENT_LAUNCH_CONTAINER"):
        parser.add_argument(
            "--ansys-version",
            dest="ansys_version",
            help=f"Specify the ansys package version to use, default is {FluentVersion.get_latest_installed().value}",
        )
        parser.add_argument(
            "--fluent-path",
            dest="fluent_path",
            help="Specify the fluent folder to use, with full path.  Such as /apps/ansys_inc/v232/fluent",
        )

    args = parser.parse_args()
    if not os.getenv("PYFLUENT_LAUNCH_CONTAINER"):
        if args.ansys_version:
            awp_root = os.environ[FluentVersion(args.ansys_version).awp_var]
            os.environ["PYFLUENT_FLUENT_ROOT"] = str(Path(awp_root) / "fluent")
        if args.fluent_path:
            os.environ["PYFLUENT_FLUENT_ROOT"] = args.fluent_path
    shutil.rmtree(GENERATED_API_DIR, ignore_errors=True)
    GENERATED_API_DIR.mkdir(exist_ok=True)
    sessions = {FluentMode.SOLVER: launch_fluent()}
    version = get_version_for_file_name(session=sessions[FluentMode.SOLVER])
    print_fluent_version.generate(sessions)
    _update_first_level(api_tree, tuigen.generate(version, sessions))
    _update_first_level(api_tree, datamodelgen.generate(version, sessions))
    _update_first_level(api_tree, settingsgen.generate(version, sessions))
    api_tree_file = get_api_tree_file_name(version)
    Path(api_tree_file).parent.mkdir(parents=True, exist_ok=True)
    with open(api_tree_file, "wb") as f:
        pickle.dump(api_tree, f)


if __name__ == "__main__":
    generate()
