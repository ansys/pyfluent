import os
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath

_THIS_DIR = os.path.dirname(__file__)


def print_fluent_version(version, pyfluent_path):
    session = pyfluent.launch_fluent()
    eval = session.scheme_eval.scheme_eval
    version_file = (
        (Path(pyfluent_path) if pyfluent_path else (Path(_THIS_DIR) / ".." / "src"))
        / "ansys"
        / "fluent"
        / "core"
        / f"fluent_version_{version}.py"
    ).resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{session.get_fluent_version()}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{eval("(inquire-build-time)")}"\n')
        f.write(f'FLUENT_BUILD_ID = "{eval("(inquire-build-id)")}"\n')
        f.write(f'FLUENT_REVISION = "{eval("(inquire-src-vcs-id)")}"\n')
        f.write(f'FLUENT_BRANCH = "{eval("(inquire-src-vcs-branch)")}"\n')
    session.exit()


def generate(version, pyfluent_path):
    print_fluent_version(version, pyfluent_path)


if __name__ == "__main__":
    version = get_version_for_filepath()
    generate(version, None)
