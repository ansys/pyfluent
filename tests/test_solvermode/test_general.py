import pytest


@pytest.mark.quick
@pytest.mark.setup
def test_solver_import_mixing_elbow(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    solver = session.solver.root
    assert solver.get_attr("active?")
    assert session.check_health() == "SERVING"
    ###
    assert not solver.setup.models.energy.enabled()
    assert session.scheme_eval.scheme_eval("(case-valid?)")
    ###
    session.solver.tui.mesh.check()
    session.solver.tui.define.units("length", "in")
    assert session.scheme_eval.scheme_eval('(units/quantity-info "length")')[-1] == "in"

    solver.setup.general.solver.get_active_child_names()

    solver.mesh.check()
    solver.setup.general.solver.time.get_attr("allowed-values")
    solver.setup.general.solver.time = "unsteady-2nd-order"
    solver.setup.general.solver.time = "unsteady-1st-order"
    solver.setup.general.solver.time = "unsteady-2nd-order-bounded"
    solver.setup.general.solver.time = "steady"

    # solver.setup.general.gravity = {"gravity": True, "y_component": -9.81}
    # solver.mesh.scale(x_scale=0.001, y_scale=0.001, z_scale=0.001)
    solver.setup.general.solver.type.get_attr("allowed-values")
    solver.setup.general.solver.type = "density-based-implicit"
    assert solver.setup.general.solver.type() == "density-based-implicit"
    solver.setup.general.solver.type = "density-based-explicit"
    assert solver.setup.general.solver.type() == "density-based-explicit"
    solver.setup.general.solver.type = "pressure-based"
    assert solver.setup.general.solver.type() == "pressure-based"

    solver.file.auto_save.data_frequency = 10
    assert solver.file.auto_save.data_frequency() == 10
    solver.file.auto_save.case_frequency = "each-time"
    assert solver.file.auto_save.case_frequency() == "each-time"
    solver.file.auto_save.root_name = "file_auto_save"
    assert solver.file.auto_save.root_name() == "file_auto_save"
    solver.setup.reference_values.compute(from_zone_name="outlet")


@pytest.mark.quick
@pytest.mark.setup
def test_disk_2d_setup(load_disk_mesh):
    session = load_disk_mesh
    solver = session.solver.root
    assert solver.get_attr("active?")
    assert session.check_health() == "SERVING"
    ###
    assert not solver.setup.models.energy.enabled()
    assert session.scheme_eval.scheme_eval("(case-valid?)")
    solver.mesh.check()
    assert solver.setup.general.solver.two_dim_space.get_attr("allowed-values") == [
        "swirl",
        "axisymmetric",
        "planar",
    ]
    assert solver.setup.general.solver.two_dim_space() == "planar"
    solver.setup.general.solver.two_dim_space = "axisymmetric"
    assert solver.setup.general.solver.two_dim_space() == "axisymmetric"
    solver.setup.general.solver.two_dim_space = "swirl"
    assert solver.setup.general.solver.two_dim_space() == "swirl"
    solver.setup.general.solver.two_dim_space = "planar"
    assert solver.setup.general.solver.two_dim_space() == "planar"
    # Bug 682773
    # solver.setup.general.gravity = {"gravity": True, "x_component": -9.81}
