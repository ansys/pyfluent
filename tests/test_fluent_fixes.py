import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples


@pytest.mark.fluent_241
def test_1364(new_solver_session):
    solver = new_solver_session

    import_filename = examples.download_file(
        "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
    )

    solver.file.read_case(file_name=import_filename)

    solver.solution.report_definitions.volume.create("xxx")

    solver.solution.report_definitions["xxx"].set_state(
        {
            "report_type": "volume-max",
            "field": "temperature",
            "average_over": 1,
            "per_zone": False,
            "zone_names": ["fluid"],
            "expr_list": None,
        }
    )

    with pytest.raises(AttributeError) as e:
        solver.solution.report_definitions.volume["xxx"].zone_names.allowed_values()
    assert e.value.args[0] == "'zone_names' object has no attribute 'allowed_values'"

    with pytest.raises(AttributeError) as e:
        solver.solution.report_definitions.volume["xxx"].expr_list.allowed_values()
    assert e.value.args[0] == "'expr_list' object has no attribute 'allowed_values'"
