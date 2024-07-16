import os
from pathlib import Path

import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_solver_import_mixingelbow(mixing_elbow_settings_session):
    solver_session = mixing_elbow_settings_session
    assert solver_session.settings.is_active()
    assert solver_session.health_check.is_serving
    file_name = Path(pyfluent.EXAMPLES_PATH) / "jou_test_general.py"
    solver_session.journal.start(file_name.as_posix())
    ###
    assert solver_session.setup.models.energy.enabled()
    scheme_eval = solver_session.scheme_eval.scheme_eval
    assert scheme_eval("(case-valid?)")
    ###
    solver_session.tui.mesh.check()
    solver_session.tui.define.units("length", "in")
    assert scheme_eval('(units/quantity-info "length")')[-1] == "in"
    general_solver = solver_session.setup.general.solver
    general_solver.time.allowed_values()
    assert general_solver.time.allowed_values() == [
        "steady",
        "unsteady-1st-order",
        "unsteady-2nd-order",
        "unsteady-2nd-order-bounded",
    ]

    general_solver.time = "unsteady-2nd-order"
    general_solver.time = "unsteady-1st-order"
    general_solver.time = "unsteady-2nd-order-bounded"
    general_solver.time = "steady"

    # solver.setup.general.gravity = {"gravity": True, "y_component": -9.81}
    # solver.mesh.scale(x_scale=0.001, y_scale=0.001, z_scale=0.001)

    assert general_solver.type.get_attr("allowed-values") == [
        "pressure-based",
        "density-based-implicit",
        "density-based-explicit",
    ]
    assert general_solver.type.allowed_values() == [
        "pressure-based",
        "density-based-implicit",
        "density-based-explicit",
    ]
    # Below line is commented due to TFS Bug 714494
    # assert solver_session.setup.general.solver.type.default_value() == "pressure-based"
    assert general_solver.type.is_active()
    assert not general_solver.type.is_read_only()
    general_solver.type = "density-based-implicit"
    assert general_solver.type() == "density-based-implicit"
    general_solver.type = "density-based-explicit"
    assert general_solver.type() == "density-based-explicit"
    general_solver.type = "pressure-based"
    assert general_solver.type() == "pressure-based"

    auto_save = solver_session.file.auto_save
    auto_save.data_frequency = 10
    assert auto_save.data_frequency.default_value() == 0
    assert auto_save.data_frequency() == 10
    auto_save.case_frequency = "each-time"
    assert auto_save.case_frequency() == "each-time"
    auto_save.root_name = "file_auto_save"
    assert auto_save.root_name() == "file_auto_save"
    solver_session.setup.reference_values.compute(
        from_zone_name="outlet", from_zone_type="pressure-outlet"
    )
    solver_session.journal.stop()
    solver_session.tui.file.read_journal(file_name.as_posix())
    assert auto_save.root_name() == "file_auto_save"
    assert general_solver.type() == "pressure-based"
    assert auto_save.data_frequency() == 10
    assert general_solver.time() == "steady"
    if os.path.exists(file_name):
        os.remove(file_name)


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_disk_2d_setup(disk_settings_session):
    session = disk_settings_session
    assert session.settings.is_active()
    assert session.health_check.is_serving
    ###
    assert not session.setup.models.energy.enabled()
    assert session.scheme_eval.scheme_eval("(case-valid?)")
    session.tui.mesh.check()

    session_solver = session.setup.general.solver
    assert session_solver.two_dim_space.get_attr("allowed-values") == [
        "swirl",
        "axisymmetric",
        "planar",
    ]
    assert session_solver.two_dim_space() == "planar"
    session_solver.two_dim_space = "axisymmetric"
    assert session_solver.two_dim_space() == "axisymmetric"
    session_solver.two_dim_space = "swirl"
    assert session_solver.two_dim_space() == "swirl"
    session_solver.two_dim_space = "planar"
    assert session_solver.two_dim_space() == "planar"
    # Bug 682773
    # session.setup.general.gravity = {"gravity": True, "x_component": -9.81}
