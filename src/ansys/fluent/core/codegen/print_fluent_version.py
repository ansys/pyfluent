"""Module to write Fluent version information."""

from ansys.fluent.core import GENERATED_API_DIR, FluentMode, launch_fluent
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name


def print_fluent_version(sessions: dict):
    """Write Fluent version information to file."""
    if FluentMode.SOLVER not in sessions:
        sessions[FluentMode.SOLVER] = launch_fluent()
    session = sessions[FluentMode.SOLVER]
    _fluent_version = session.get_fluent_version().value
    version_for_filename = get_version_for_file_name(_fluent_version)
    eval = session.scheme_eval.scheme_eval
    version_file = (
        GENERATED_API_DIR / f"fluent_version_{version_for_filename}.py"
    ).resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{_fluent_version}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{eval("(inquire-build-time)")}"\n')
        f.write(f'FLUENT_BUILD_ID = "{eval("(inquire-build-id)")}"\n')
        f.write(f'FLUENT_REVISION = "{eval("(inquire-src-vcs-id)")}"\n')
        f.write(f'FLUENT_BRANCH = "{eval("(inquire-src-vcs-branch)")}"\n')


def generate(sessions: dict):
    """Write Fluent version information."""
    print_fluent_version(sessions)


if __name__ == "__main__":
    generate(None, {})
