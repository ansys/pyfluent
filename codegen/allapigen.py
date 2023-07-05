import argparse
import os
from pathlib import Path

import datamodelgen
import print_fluent_version
import settingsgen
import tuigen

from ansys.fluent.core.launcher.launcher import FluentVersion, get_ansys_version

if __name__ == "__main__":
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

    print_fluent_version.generate()
    tuigen.generate()
    datamodelgen.generate()
    settingsgen.generate()
