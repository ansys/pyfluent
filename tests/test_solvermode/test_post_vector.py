import pytest
@pytest.mark.setup
def test_post_elbow(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    # below commands to be removed when data load step is added
    session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag = {
        "option": "constant or expression",
        "constant": 0.4,
    }
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_intensity = 5
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_hydraulic_diam = "4 [in]"
    session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].t = {
        "option": "constant or expression",
        "constant": 293.15,
    }
    session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"].vmag = {
        "option": "constant or expression",
        "constant": 1.2,
    }
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].turb_hydraulic_diam = "1 [in]"
    session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"].t = {
        "option": "constant or expression",
        "constant": 313.15,
    }
    session.solver.root.setup.boundary_conditions.pressure_outlet[
        "outlet"
    ].turb_viscosity_ratio = 4
    session.solver.tui.solve.monitors.residual.plot("no")
    session.solver.root.solution.initialization.hybrid_initialize()
    session.solver.root.solution.run_calculation.iterate.get_attr("arguments")
    session.solver.root.solution.run_calculation.number_of_iterations = 5
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=5)

    # Above commands to be removed when data load step is added

    session.solver.root.results.graphics.vector["velocity_vector_symmetry"] = {}
    session.solver.root.results.graphics.vector[
        "velocity_vector_symmetry"
    ].field = "temperature"
    session.solver.root.results.graphics.vector[
        "velocity_vector_symmetry"
    ].surfaces_list = [
        "symmetry-xyplane",
    ]
    session.solver.root.results.graphics.vector[
        "velocity_vector_symmetry"
    ].scale.scale_f = 4
    session.solver.root.results.graphics.vector["velocity_vector_symmetry"].style = "arrow"

    vel_vector = session.solver.root.results.graphics.vector["velocity_vector_symmetry"]()
    assert vel_vector.get('name') == 'velocity_vector_symmetry'
    assert vel_vector.get('field') == 'temperature'
    assert vel_vector.get('surfaces_list') == ['symmetry-xyplane']
    assert vel_vector.get('scale') == {'auto_scale': True, 'scale_f': 4.0}
    assert vel_vector.get('style') == 'arrow'