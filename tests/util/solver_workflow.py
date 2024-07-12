import pytest


@pytest.fixture
def new_solver_session_single_precision():
    solver = create_solver_session(precision="single")
    yield solver
    solver.exit(timeout=5, timeout_force=True)
