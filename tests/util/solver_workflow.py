import pytest

import ansys.fluent.core as pyfluent


def create_solver_session(*args, **kwargs):
    return pyfluent.launch_fluent(**kwargs)


@pytest.fixture
def new_solver_session(with_running_pytest):
    # import time
    # time.sleep(20)
    solver = create_solver_session()
    yield solver
    solver.exit()


@pytest.fixture
def new_solver_session_no_transcript(with_running_pytest):
    solver = create_solver_session(start_transcript=False)
    yield solver
    solver.exit()
