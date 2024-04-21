"""Provides a module for generating Fluent datamodel result files."""

from ansys.fluent.core import FluentMode, launch_fluent
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name
from codegen.datamodelgen import generate

if __name__ == "__main__":
    sessions = {FluentMode.SOLVER: launch_fluent()}
    version = get_version_for_file_name(session=sessions[FluentMode.SOLVER])
    generate(version, None, sessions, True, False)
