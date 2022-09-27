import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.fluent_version import get_version, get_version_for_filepath

_THIS_DIR = os.path.dirname(__file__)


def print_fluent_version():
    session = pyfluent.launch_fluent(mode="solver")
    eval = session.scheme_eval.scheme_eval
    version_file = os.path.join(
        _THIS_DIR,
        "..",
        "src",
        "ansys",
        "fluent",
        "core",
        f"fluent_version_{get_version_for_filepath()}.py",
    )
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{get_version()}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{eval("(inquire-build-time)")}"\n')
        f.write(f'FLUENT_BUILD_ID = "{eval("(inquire-build-id)")}"\n')
        f.write(f'FLUENT_REVISION = "{eval("(inquire-src-vcs-id)")}"\n')
        f.write(f'FLUENT_BRANCH = "{eval("(inquire-src-vcs-branch)")}"\n')
    session.exit()


def generate():
    print_fluent_version()


if __name__ == "__main__":
    generate()
