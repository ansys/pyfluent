import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy


def create_solver_session(*args, **kwargs):
    if pyfluent.USE_FILE_TRANSFER_SERVICE:
        container_dict = {"host_mount_path": pyfluent.USER_DATA_PATH}
        file_transfer_service = RemoteFileTransferStrategy()
        return pyfluent.launch_fluent(
            container_dict=container_dict,
            file_transfer_service=file_transfer_service,
            **kwargs,
        )
    else:
        return pyfluent.launch_fluent(**kwargs)


@pytest.fixture
def new_solver_session():
    solver = create_solver_session()
    yield solver
    solver.exit(timeout=5, timeout_force=True)


@pytest.fixture
def make_new_session():
    sessions = []

    def _make_new_session(**kwargs):
        if pyfluent.USE_FILE_TRANSFER_SERVICE:
            container_dict = {"host_mount_path": pyfluent.USER_DATA_PATH}
            file_transfer_service = RemoteFileTransferStrategy()
            session = pyfluent.launch_fluent(
                container_dict=container_dict,
                file_transfer_service=file_transfer_service,
                **kwargs,
            )
        else:
            session = pyfluent.launch_fluent(**kwargs)
        sessions.append(session)
        return session

    yield _make_new_session

    for session in sessions:
        session.exit(timeout=5, timeout_force=True)


@pytest.fixture
def new_solver_session_single_precision():
    solver = create_solver_session(precision="single")
    yield solver
    solver.exit(timeout=5, timeout_force=True)


@pytest.fixture
def new_solver_session_no_transcript():
    solver = create_solver_session(start_transcript=False, mode="solver")
    yield solver
    solver.exit(timeout=5, timeout_force=True)
