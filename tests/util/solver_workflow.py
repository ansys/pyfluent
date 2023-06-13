import pytest

import ansys.fluent.core as pyfluent


def create_solver_session(*args, **kwargs):
    return pyfluent.launch_fluent(**kwargs)


@pytest.fixture
def new_solver_session(with_launching_container):
    solver = create_solver_session()
    yield solver
    solver.exit(timeout=5, timeout_force=True)


@pytest.fixture
def new_solver_session_single_precision(with_launching_container):
    solver = create_solver_session(precision="single")
    yield solver
    solver.exit(timeout=5, timeout_force=True)


@pytest.fixture
def new_solver_session_no_transcript(with_launching_container):
    solver = create_solver_session(start_transcript=False, mode="solver")
    yield solver
    solver.exit(timeout=5, timeout_force=True)
