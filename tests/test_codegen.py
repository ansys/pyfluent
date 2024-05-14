import importlib
import pickle

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core.codegen import allapigen
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name
from ansys.fluent.core.utils.search import get_api_tree_file_name


@pytest.mark.codegen_required
def test_allapigen_files(new_solver_session):
    version = get_version_for_file_name(session=new_solver_session)
    importlib.import_module(f"ansys.fluent.core.generated.fluent_version_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.meshing.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.solver.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.datamodel_{version}.meshing")
    importlib.import_module(f"ansys.fluent.core.generated.datamodel_{version}.workflow")
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.preferences"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.PartManagement"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.PMFileManagement"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.solver.settings_{version}.root"
    )


def test_codegen_with_no_static_info(tmp_path, monkeypatch):
    codegen_outdir = tmp_path / "generated"
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    allapigen.generate(version, {})
    generted_paths = list(codegen_outdir.glob("*"))
    assert len(generted_paths) == 1
    assert set(p.name for p in generted_paths) == {f"api_tree_{version}.pickle"}
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    assert api_tree == {
        "<meshing_session>": {"tui": {}},
        "<solver_session>": {"tui": {}},
    }
