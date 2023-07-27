import json
import os
from unittest import TestCase

import pytest
from util.fixture_fluent import get_name_info
from util.solver import SettingsValDict as D
from util.solver import assign_settings_value_from_value_dict as assign_dict_val


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
@pytest.mark.integration
@pytest.mark.setup
@pytest.mark.codegen_required
def test_boundaries_elbow(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    solver_session.setup.models.energy.enabled = True
    assert (
        D(0)
        == solver_session.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag()
    )
    assign_dict_val(
        solver_session.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag, 0.4
    )
    assert (
        D(0.4)
        == solver_session.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag()
    )
    solver_session.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    solver_session.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_intensity = 0.05
    solver_session.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_hydraulic_diam = "4 [in]"
    assign_dict_val(
        solver_session.setup.boundary_conditions.velocity_inlet["cold-inlet"].t, 293.15
    )
    assert {
        "name": "cold-inlet",
        "velocity_spec": "Magnitude, Normal to Boundary",
        "frame_of_reference": "Absolute",
        "vmag": {"option": "value", "value": 0.4},
        "initial_gauge_pressure": {"option": "value", "value": 0},
        "t": {"option": "value", "value": 293.15},
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_intensity": 0.05,
        "turb_hydraulic_diam": "4 [in]",
    } == solver_session.setup.boundary_conditions.velocity_inlet["cold-inlet"]()

    assign_dict_val(
        solver_session.setup.boundary_conditions.velocity_inlet["hot-inlet"].vmag, 1.2
    )
    solver_session.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    solver_session.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].turb_hydraulic_diam = "1 [in]"
    assign_dict_val(
        solver_session.setup.boundary_conditions.velocity_inlet["hot-inlet"].t, 313.15
    )
    assert {
        "name": "hot-inlet",
        "velocity_spec": "Magnitude, Normal to Boundary",
        "frame_of_reference": "Absolute",
        "vmag": {"option": "value", "value": 1.2},
        "initial_gauge_pressure": {"option": "value", "value": 0},
        "t": {"option": "value", "value": 313.15},
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_intensity": 0.05,
        "turb_hydraulic_diam": "1 [in]",
    } == solver_session.setup.boundary_conditions.velocity_inlet["hot-inlet"]()

    solver_session.setup.boundary_conditions.pressure_outlet[
        "outlet"
    ].turb_viscosity_ratio = 4
    assert (
        solver_session.setup.boundary_conditions.pressure_outlet[
            "outlet"
        ].turb_viscosity_ratio()
        == 4
    )


# TODO: Skipped for the nightly test run to be successful. Later decide what to do with this test (discard?).
@pytest.mark.nightly
@pytest.mark.integration
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
@pytest.mark.skip
def test_boundaries_periodic(load_periodic_rot_cas):
    solver_session = load_periodic_rot_cas
    print(__file__)
    _THIS_DIR = os.path.dirname(__file__)
    _DATA_FILE = os.path.join(_THIS_DIR, "boundaries_periodic_expDict")
    boundary_exp = json.load(open(_DATA_FILE))
    boundary_test = dict()
    boundary_tested = dict()
    for name, boundary in solver_session.setup.boundary_conditions.items():
        boundary_test[name] = boundary()
    boundary_tested["val_1"] = boundary_test
    TestCase().assertDictEqual(boundary_tested["val_1"], boundary_exp["val_1"])

    boundary_test = dict()
    for (
        boundary_type
    ) in solver_session.setup.boundary_conditions.get_active_child_names():
        if boundary_type == "matching_tolerance":
            continue
        for name, boundary in getattr(
            solver_session.setup.boundary_conditions, boundary_type
        ).items():
            boundary_test[name] = boundary()
    boundary_tested["val_2"] = boundary_test
    TestCase().assertDictEqual(boundary_tested["val_2"], boundary_exp["val_2"])

    boundaries_check = ["inlet", "outlet", "pipe_2_wall"]
    selected_bou_test = get_name_info(boundary_tested["val_1"], boundaries_check)
    selected_bou_exp = get_name_info(boundary_exp["val_1"], boundaries_check)
    TestCase().assertDictEqual(selected_bou_test, selected_bou_exp)
    # commented new method due to bug 753
    # solver_session.setup.boundary_conditions.wall["pipe_2_wall"].rename("pipe2_wall")
    solver_session.setup.boundary_conditions.wall.rename("pipe2_wall", "pipe_2_wall")
    solver_session.setup.boundary_conditions.wall.rename("out", "outlet")
    solver_session.setup.boundary_conditions.velocity_inlet["inlet"].vmag = 5.0
    solver_session.setup.boundary_conditions["inlet"].vmag = 10.0
    boundaries_check = ["inlet", "out", "pipe2_wall"]
    boundary_test = dict()
    for name, boundary in solver_session.setup.boundary_conditions.items():
        boundary_test[name] = boundary()
    boundary_tested["val_3"] = boundary_test
    TestCase().assertDictEqual(boundary_tested["val_3"], boundary_exp["val_3"])

    selected_bou_test = get_name_info(boundary_tested["val_3"], boundaries_check)
    selected_bou_exp = get_name_info(boundary_exp["val_3"], boundaries_check)
    TestCase().assertDictEqual(selected_bou_test, selected_bou_exp)
    with open("boundaries_periodic_outDict.py", "a") as f:
        json.dump(boundary_tested, f, sort_keys=True, indent=4)
