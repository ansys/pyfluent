import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file

def create_solver_session(*args, **kwargs):
    return pyfluent.launch_fluent(**kwargs)


@pytest.fixture
def new_solver_session(with_launching_container):
    solver = create_solver_session()
    yield solver
    solver.exit()


@pytest.fixture
def new_solver_session_no_transcript(with_launching_container):
    solver = create_solver_session(start_transcript=False)
    yield solver
    solver.exit()