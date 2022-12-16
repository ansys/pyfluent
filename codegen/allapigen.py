import argparse
import os

import datamodelgen
import print_fluent_version
import settingsgen
import tuigen

from ansys.fluent.core.launcher.launcher import (
    FLUENT_VERSION,
    set_ansys_version,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate python code from Fluent APIs"
    )
    parser.add_argument(
        "--ansys-version",
        dest="ansys_version",
        help=f"Specify the ansys package version to use, default is {FLUENT_VERSION}",
    )
    parser.add_argument(
        "--fluent-path",
        dest="fluent_path",
        help="Specify the fluent folder to use, with full path.  Such as /apps/ansys_inc/v231/fluent",
    )
    args = parser.parse_args()

    if args.ansys_version:
        set_ansys_version(args.ansys_version)
    if args.fluent_path:
        os.environ["PYFLUENT_FLUENT_ROOT"] = args.fluent_path

    print_fluent_version.generate()
    tuigen.generate()
    datamodelgen.generate()
    settingsgen.generate()
