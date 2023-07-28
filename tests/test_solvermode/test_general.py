import os
from pathlib import Path

import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.skip("Fluent side bug")
@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version("dev")
def test_solver_import_mixingelbow(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    assert solver_session._root.is_active()
    assert solver_session.health_check_service.is_serving
    file_path = Path(pyfluent.EXAMPLES_PATH) / "jou_test_general.py"
    solver_session.journal.start(file_path.as_posix())
    ###
    assert not solver_session.setup.models.energy.enabled()
    assert solver_session.scheme_eval.scheme_eval("(case-valid?)")
    ###
    solver_session.tui.mesh.check()
    solver_session.tui.define.units("length", "in")
    assert (
        solver_session.scheme_eval.scheme_eval('(units/quantity-info "length")')[-1]
        == "in"
    )
    solver_session.setup.general.solver.time.allowed_values()
    assert solver_session.setup.general.solver.time.allowed_values() == [
        "steady",
        "unsteady-1st-order",
        "unsteady-2nd-order",
        "unsteady-2nd-order-bounded",
    ]
    solver_session.setup.general.solver.time = "unsteady-2nd-order"
    solver_session.setup.general.solver.time = "unsteady-1st-order"
    solver_session.setup.general.solver.time = "unsteady-2nd-order-bounded"
    solver_session.setup.general.solver.time = "steady"

    # solver.setup.general.gravity = {"gravity": True, "y_component": -9.81}
    # solver.mesh.scale(x_scale=0.001, y_scale=0.001, z_scale=0.001)
    assert solver_session.setup.general.solver.type.get_attr("allowed-values") == [
        "pressure-based",
        "density-based-implicit",
        "density-based-explicit",
    ]
    assert solver_session.setup.general.solver.type.allowed_values() == [
        "pressure-based",
        "density-based-implicit",
        "density-based-explicit",
    ]
    # Below line is commented due to TFS Bug 714494
    # assert solver_session.setup.general.solver.type.default_value() == "pressure-based"
    assert solver_session.setup.general.solver.type.is_active()
    assert not solver_session.setup.general.solver.type.is_read_only()
    solver_session.setup.general.solver.type = "density-based-implicit"
    assert solver_session.setup.general.solver.type() == "density-based-implicit"
    solver_session.setup.general.solver.type = "density-based-explicit"
    assert solver_session.setup.general.solver.type() == "density-based-explicit"
    solver_session.setup.general.solver.type = "pressure-based"
    assert solver_session.setup.general.solver.type() == "pressure-based"

    solver_session.file.auto_save.data_frequency = 10
    assert solver_session.file.auto_save.data_frequency.default_value() == 0
    assert solver_session.file.auto_save.data_frequency() == 10
    solver_session.file.auto_save.case_frequency = "each-time"
    assert solver_session.file.auto_save.case_frequency() == "each-time"
    solver_session.file.auto_save.root_name = "file_auto_save"
    assert solver_session.file.auto_save.root_name() == "file_auto_save"
    solver_session.setup.reference_values.compute(from_zone_name="outlet")
    solver_session.journal.stop()
    solver_session.tui.file.read_journal(file_path.as_posix())
    assert solver_session.file.auto_save.root_name() == "file_auto_save"
    assert solver_session.setup.general.solver.type() == "pressure-based"
    assert solver_session.file.auto_save.data_frequency() == 10
    assert solver_session.setup.general.solver.time() == "steady"
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version("dev")
def test_disk_2d_setup(load_disk_mesh):
    session = load_disk_mesh
    assert session._root.get_attr("active?")
    assert session.health_check_service.is_serving
    ###
    assert not session.setup.models.energy.enabled()
    assert session.scheme_eval.scheme_eval("(case-valid?)")
    session.tui.mesh.check()
    assert session.setup.general.solver.two_dim_space.get_attr("allowed-values") == [
        "swirl",
        "axisymmetric",
        "planar",
    ]
    assert session.setup.general.solver.two_dim_space() == "planar"
    session.setup.general.solver.two_dim_space = "axisymmetric"
    assert session.setup.general.solver.two_dim_space() == "axisymmetric"
    session.setup.general.solver.two_dim_space = "swirl"
    assert session.setup.general.solver.two_dim_space() == "swirl"
    session.setup.general.solver.two_dim_space = "planar"
    assert session.setup.general.solver.two_dim_space() == "planar"
    # Bug 682773
    # session.setup.general.gravity = {"gravity": True, "x_component": -9.81}
