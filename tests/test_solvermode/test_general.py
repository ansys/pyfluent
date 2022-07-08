import pytest


@pytest.mark.quick
@pytest.mark.setup
def test_solver_import_mixingelbow(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    assert session.solver.root.get_attr("active?")
    assert session.check_health() == "SERVING"
    ###
    assert not session.solver.root.setup.models.energy.enabled()
    assert session.scheme_eval.scheme_eval("(case-valid?)")
    ###
    session.solver.tui.mesh.check()
    session.solver.tui.define.units("length", "in")
    assert session.scheme_eval.scheme_eval('(units/quantity-info "length")')[-1] == "in"
