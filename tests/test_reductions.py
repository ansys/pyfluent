import pytest
from util.fixture_fluent import sample_solver_session  # noqa: F401

from ansys.fluent.core import examples


@pytest.mark.fluent_231
def test_reductions(sample_solver_session) -> None:
    solver = sample_solver_session
    case_filepath = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=case_filepath)
    # input_type, input_name = download_input_file(
    #    "pyfluent/mixing_elbow", "mixing_elbow.cas.h5", "mixing_elbow.dat.h5"
    # )
    # solver.file.read(file_type=input_type, file_name=input_name)
