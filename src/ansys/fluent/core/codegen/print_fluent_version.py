"""Module to write Fluent version information."""

from ansys.fluent.core import CODEGEN_OUTDIR, FluentVersion, launch_fluent


def print_fluent_version(app_utilities):
    """Write Fluent version information to file."""
    version = FluentVersion(app_utilities.get_product_version()).number
    build_info = app_utilities.get_build_info()
    version_file = (CODEGEN_OUTDIR / f"fluent_version_{version}.py").resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{version}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{build_info["build_time"]}"\n')
        f.write(f'FLUENT_BUILD_ID = "{build_info["build_id"]}"\n')
        f.write(f'FLUENT_REVISION = "{build_info["vcs_revision"]}"\n')
        f.write(f'FLUENT_BRANCH = "{build_info["vcs_branch"]}"\n')


if __name__ == "__main__":
    solver = launch_fluent()
    print_fluent_version(solver._app_utilities)
