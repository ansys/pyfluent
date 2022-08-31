import sys

import ansys.fluent.core as pyfluent


def setup_for_fluent(version: str, mode: str):
    session = pyfluent.launch_fluent(mode=mode)
    globals()["solver"] = session


script_file = sys.argv[1]
exec(open(script_file).read())
