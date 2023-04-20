from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples


def test_1364(new_solver_session):
    solver = new_solver_session

    import_filename = examples.download_file(
        "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
    )

    solver.file.read_case(file_name=import_filename)

    solver.solution.report_definitions.volume.create("xxx")

    assert (
        solver.solution.report_definitions.volume["xxx"].expr_list.allowed_values()
        == None
    )
