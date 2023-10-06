import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples


@pytest.mark.nightly
@pytest.mark.fluent_version("==23.2")
def test_1364(new_solver_session):
    solver = new_solver_session

    import_filename = examples.download_file(
        "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
    )

    solver.file.read_case(file_name=import_filename)

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
