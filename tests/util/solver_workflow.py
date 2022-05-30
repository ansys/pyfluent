import pytest

import ansys.fluent.core as pyfluent


def create_solver_session():
    return pyfluent.launch_fluent()


@pytest.fixture
def new_solver_session(with_running_pytest):
    # import time
    # time.sleep(20)
    solver = create_solver_session()
    yield solver
    solver.exit()
