import os
from pathlib import Path

from ansys.fluent.core import FluentMode, launch_fluent
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name

_THIS_DIR = os.path.dirname(__file__)


def print_fluent_version(pyfluent_path, sessions: dict):
    if FluentMode.SOLVER not in sessions:
        sessions[FluentMode.SOLVER] = launch_fluent()
    session = sessions[FluentMode.SOLVER]
    fluent_version = session.get_fluent_version().value
    version_for_filename = get_version_for_file_name(fluent_version)
    eval = session.scheme_eval.scheme_eval
    version_file = (
        (Path(pyfluent_path) if pyfluent_path else (Path(_THIS_DIR) / ".." / "src"))
        / "ansys"
        / "fluent"
        / "core"
        / f"fluent_version_{version_for_filename}.py"
    ).resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{fluent_version}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{eval("(inquire-build-time)")}"\n')
        f.write(f'FLUENT_BUILD_ID = "{eval("(inquire-build-id)")}"\n')
        f.write(f'FLUENT_REVISION = "{eval("(inquire-src-vcs-id)")}"\n')
        f.write(f'FLUENT_BRANCH = "{eval("(inquire-src-vcs-branch)")}"\n')


def generate(pyfluent_path, sessions: dict):
    print_fluent_version(pyfluent_path, sessions)


if __name__ == "__main__":
    generate(None, {})
