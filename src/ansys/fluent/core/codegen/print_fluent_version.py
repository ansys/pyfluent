"""Module to write Fluent version information."""

from ansys.fluent.core import CODEGEN_OUTDIR, launch_fluent
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name


def print_fluent_version(version: str, scheme_eval):
    """Write Fluent version information to file."""
    version_file = (CODEGEN_OUTDIR / f"fluent_version_{version}.py").resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{version}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{scheme_eval("(inquire-build-time)")}"\n')
        f.write(f'FLUENT_BUILD_ID = "{scheme_eval("(inquire-build-id)")}"\n')
        f.write(f'FLUENT_REVISION = "{scheme_eval("(inquire-src-vcs-id)")}"\n')
        f.write(f'FLUENT_BRANCH = "{scheme_eval("(inquire-src-vcs-branch)")}"\n')


def generate(version: str, scheme_eval):
    """Write Fluent version information."""
    print_fluent_version(version, scheme_eval)


if __name__ == "__main__":
    solver = launch_fluent()
    version = get_version_for_file_name(session=solver)
    generate(version, solver.scheme_eval.scheme_eval)
