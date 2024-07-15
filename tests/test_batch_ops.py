import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


@pytest.mark.fluent_version(">=24.1")
def test_batch_ops_create_mesh(new_solver_session):
    solver = new_solver_session
    mesh = solver.results.graphics.mesh
    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    with pyfluent.BatchOps(solver):
        solver.file.read(
            file_name=case_file_name, file_type="case", lightweight_setup=True
        )
        mesh["mesh-1"] = {}
        assert not solver.scheme_eval.scheme_eval("(case-valid?)")
        assert "mesh-1" not in mesh.get_object_names()
    assert solver.scheme_eval.scheme_eval("(case-valid?)")
    assert "mesh-1" in mesh.get_object_names()


@pytest.mark.fluent_version(">=24.1")
def test_batch_ops_create_mesh_and_access_fails(new_solver_session):
    solver = new_solver_session
    mesh = solver.results.graphics.mesh
    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    with pytest.raises(KeyError):
        with pyfluent.BatchOps(solver):
            solver.file.read(
                file_name=case_file_name, file_type="case", lightweight_setup=True
            )
            mesh["mesh-1"] = {}
            mesh["mesh-1"].surfaces_list = ["wall-elbow"]
    assert not solver.scheme_eval.scheme_eval("(case-valid?)")
