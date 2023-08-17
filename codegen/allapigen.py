import argparse
import collections
import os
from pathlib import Path

# import pickle
from pprint import pprint

# import datamodelgen
import print_fluent_version

# import settingsgen
import tuigen

from ansys.fluent.core.launcher.launcher import FluentVersion, get_ansys_version
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath
from ansys.fluent.core.utils.search import get_api_tree_filepath


def _update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = _update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


if __name__ == "__main__":
    api_tree = {}
    if not os.getenv("PYFLUENT_LAUNCH_CONTAINER"):
        parser = argparse.ArgumentParser(
            description="Generate python code from Fluent APIs"
        )
        parser.add_argument(
            "--ansys-version",
            dest="ansys_version",
            help=f"Specify the ansys package version to use, default is {get_ansys_version()}",
        )
        parser.add_argument(
            "--fluent-path",
            dest="fluent_path",
            help="Specify the fluent folder to use, with full path.  Such as /apps/ansys_inc/v232/fluent",
        )
        args = parser.parse_args()

        if args.ansys_version:
            awp_root = os.environ[
                "AWP_ROOT"
                + "".join(str(FluentVersion(args.ansys_version)).split("."))[:-1]
            ]
            os.environ["PYFLUENT_FLUENT_ROOT"] = str(Path(awp_root) / "fluent")
        if args.fluent_path:
            os.environ["PYFLUENT_FLUENT_ROOT"] = args.fluent_path
    version = get_version_for_filepath()
    print_fluent_version.generate(version)
    _update(api_tree, tuigen.generate(version))
    # datamodelgen.generate()
    # settingsgen.generate()
    api_tree_file = get_api_tree_filepath(version)
    Path(api_tree_file).parent.mkdir(parents=True, exist_ok=True)
    with open(api_tree_file, "w") as f:
        # pickle.dump(api_tree, f)
        pprint(api_tree, f)
