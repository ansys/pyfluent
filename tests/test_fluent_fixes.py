import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples


@pytest.mark.nightly
@pytest.mark.fluent_version("==23.2")
def test_1364(new_solver_session):
    solver = new_solver_session

    import_file_name = examples.download_file(
        "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
    )

    solver.file.read_case(file_name=import_file_name)

    report_def = solver.solution.report_definitions.volume.create("xxx")

    report_def.set_state(
        {
            "report_type": "volume-max",
            "field": "temperature",
            "average_over": 1,
            "per_zone": False,
            "zone_names": ["fluid"],
            "expr_list": None,
        }
    )

    assert report_def.zone_names.allowed_values() == ["fluid"]

    assert report_def.expr_list.allowed_values() == None


def test_637_974_1744(new_solver_session):
    solver_session = new_solver_session

    import_case = examples.download_file(
        file_name="exhaust_system.cas.h5", directory="pyfluent/exhaust_system"
    )

    import_data = examples.download_file(
        file_name="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
    )

    solver_session.tui.file.read_case(import_case)

    solver_session.tui.file.read_data(import_data)

    solver_session.tui.solve.set.number_of_iterations(15)
    solver_session.tui.solve.iterate()

    monitors_list = solver_session.monitors_manager.get_monitor_set_names()

    assert monitors_list == [
        "residual",
        "mass-bal-rplot",
        "mass-tot-rplot",
        "mass-in-rplot",
        "point-vel-rplot",
    ]

    mp = solver_session.monitors_manager.get_monitor_set_data(
        monitor_set_name="residual"
    )

    assert mp
