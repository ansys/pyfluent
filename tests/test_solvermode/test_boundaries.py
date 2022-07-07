import pytest
@pytest.mark.integration
def test_boundaries_elbow(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    assert session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag() == {'option': 'constant or expression', 'constant': 0}
    session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag = {
    "option": "constant or expression",
    "constant": 0.4,}
    assert session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag() == {'option': 'constant or expression', 'constant': 0.4}

    session.solver.root.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"].ke_spec = "Intensity and Hydraulic Diameter"
    session.solver.root.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"].turb_intensity = 5
    session.solver.root.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"].turb_hydraulic_diam = "4 [in]"
    session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].t = {
    "option": "constant or expression",
    "constant": 293.15,}
    assert session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"]() == {'velocity_spec': 'Magnitude, Normal to Boundary','frame_of_reference': 'Absolute','vmag': {'option': 'constant or expression', 'constant': 0.4},'p_sup': {'option': 'constant or expression', 'constant': 0},'t': {'option': 'constant or expression', 'constant': 293.15},'ke_spec': 'Intensity and Hydraulic Diameter','turb_intensity': 5,'turb_hydraulic_diam': {'constant': 1, 'expression': '4 [in]'}}
    session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"].vmag = {
    "option": "constant or expression",
    "constant": 1.2,}
    session.solver.root.setup.boundary_conditions.velocity_inlet[
    "hot-inlet"].ke_spec = "Intensity and Hydraulic Diameter"
    session.solver.root.setup.boundary_conditions.velocity_inlet[
    "hot-inlet"].turb_hydraulic_diam = "1 [in]"
    session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"].t = {
    "option": "constant or expression",
    "constant": 313.15,}
    assert session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"]() == {'velocity_spec': 'Magnitude, Normal to Boundary','frame_of_reference': 'Absolute','vmag': {'option': 'constant or expression', 'constant': 1.2},'p_sup': {'option': 'constant or expression', 'constant': 0},'t': {'option': 'constant or expression', 'constant': 313.15},'ke_spec': 'Intensity and Hydraulic Diameter','turb_intensity': 0.05,'turb_hydraulic_diam': {'expression': '1 [in]', 'constant': 1}}
    session.solver.root.setup.boundary_conditions.pressure_outlet[
    "outlet"].turb_viscosity_ratio = 4
    assert session.solver.root.setup.boundary_conditions.pressure_outlet["outlet"].turb_viscosity_ratio() == 4