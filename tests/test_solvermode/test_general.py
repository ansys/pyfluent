import pytest


@pytest.mark.quick
@pytest.mark.setup
def test_solver_import_mixingelbow(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    assert solver_session.root.get_attr("active?")
    assert solver_session.check_health() == "SERVING"
    ###
    assert not solver_session.root.setup.models.energy.enabled()
    assert solver_session.scheme_eval.scheme_eval("(case-valid?)")
    ###
    solver_session.tui.mesh.check()
    solver_session.tui.define.units("length", "in")
    assert (
        solver_session.scheme_eval.scheme_eval('(units/quantity-info "length")')[-1]
        == "in"
    )
