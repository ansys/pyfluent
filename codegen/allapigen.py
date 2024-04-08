import argparse
import os
from pathlib import Path
import pickle

import datamodelgen
import print_fluent_version
import settingsgen
import tuigen

from ansys.fluent.core import FluentMode, launch_fluent
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)
from ansys.fluent.core.utils.search import get_api_tree_file_name


def _update_first_level(d, u):
    for k in d:
        d[k].update(u.get(k, {}))


if __name__ == "__main__":
    api_tree = {"<meshing_session>": {}, "<solver_session>": {}}
    parser = argparse.ArgumentParser(
        description="Generate python code from Fluent APIs"
    )
    parser.add_argument(
        "--pyfluent-path",
        dest="pyfluent_path",
        help="Specify the pyfluent installation folder to patch, with full path.  Such as /my-venv/Lib/site-packages",
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
    sessions = {FluentMode.SOLVER: launch_fluent()}
    version = get_version_for_file_name(session=sessions[FluentMode.SOLVER])
    print_fluent_version.generate(args.pyfluent_path, sessions)
    _update_first_level(
        api_tree, tuigen.generate(version, args.pyfluent_path, sessions)
    )
    _update_first_level(
        api_tree,
        datamodelgen.generate(
            version, args.pyfluent_path, sessions, generate_rst=False, generate_py=True
        ),
    )
    _update_first_level(
        api_tree, settingsgen.generate(version, args.pyfluent_path, sessions)
    )
    api_tree_file = get_api_tree_file_name(version, args.pyfluent_path)
    Path(api_tree_file).parent.mkdir(parents=True, exist_ok=True)
    with open(api_tree_file, "wb") as f:
        pickle.dump(api_tree, f)
