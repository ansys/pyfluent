import importlib

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.utils.fluent_version import get_version_for_file_name


@pytest.mark.codegen_required
def test_allapigen_files(new_solver_session):
    version = get_version_for_file_name(session=new_solver_session)
    importlib.import_module(f"ansys.fluent.core.fluent_version_{version}")
    importlib.import_module(f"ansys.fluent.core.meshing.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.solver.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.datamodel_{version}.meshing")
    importlib.import_module(f"ansys.fluent.core.datamodel_{version}.workflow")
    importlib.import_module(f"ansys.fluent.core.datamodel_{version}.preferences")
    importlib.import_module(f"ansys.fluent.core.datamodel_{version}.PartManagement")
    importlib.import_module(f"ansys.fluent.core.datamodel_{version}.PMFileManagement")
    importlib.import_module(f"ansys.fluent.core.solver.settings_{version}.root")
