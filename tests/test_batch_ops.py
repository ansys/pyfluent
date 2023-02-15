import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.api.fluent.v0 import batch_ops_pb2
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


@pytest.mark.dev
@pytest.mark.fluent_232
@pytest.mark.skip("Failing in github")
def test_batch_ops(new_solver_session):
    import_filename = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    with pyfluent.BatchOps(new_solver_session):
        assert len(pyfluent.BatchOps.instance()._ops) == 0
        new_solver_session.tui.file.read_case(import_filename)
        new_solver_session.setup.models.energy.enabled = False
        assert len(pyfluent.BatchOps.instance()._ops) == 2
    assert all(op._status == batch_ops_pb2.STATUS_SUCCESSFUL for op in pyfluent.BatchOps.instance()._ops)
