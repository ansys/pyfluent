"""Module to write Fluent version information."""

from ansys.fluent.core import CODEGEN_OUTDIR, launch_fluent
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name


def print_fluent_version(version: str, app_utilities):
    """Write Fluent version information to file."""
    version_file = (CODEGEN_OUTDIR / f"fluent_version_{version}.py").resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{version}"\n')
        f.write(f'"{app_utilities.get_build_info()}"\n')


def generate(version: str, app_utilities):
    """Write Fluent version information."""
    print_fluent_version(version, app_utilities)


if __name__ == "__main__":
    solver = launch_fluent()
    version = get_version_for_file_name(session=solver)
    generate(version, solver._app_utilities)
