import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file


def assign_task_arguments(
    workflow, check_state: bool, task_name: str, **kwargs
) -> None:
    task = workflow.TaskObject[task_name]
    task.Arguments = kwargs
    if check_state:
        # the state that we have set must be a subset of the total state
        assert kwargs.items() <= task.Arguments().items()


def check_task_execute_preconditions(task) -> None:
    assert task.State() == "Out-of-date"
    assert not task.Errors() or not len(task.Errors())


def check_task_execute_postconditions(task) -> None:
    assert task.State() == "Up-to-date"
    assert not task.Errors() or not len(task.Errors())


def execute_task_with_pre_and_postcondition_checks(workflow, task_name: str) -> None:
    task = workflow.TaskObject[task_name]
    check_task_execute_preconditions(task)
    # Some tasks are wrongly returning False in meshing workflow itself
    # so we add a temporary caveat below
    result = task.Execute()
    if task_name not in (
        "Add Local Sizing",
        "Add Boundary Layers",
        "Import CAD and Part Management",
    ):
        assert result is True
    check_task_execute_postconditions(task)


def create_mesh_session():
    return pyfluent.launch_fluent(mode="meshing", precision="double", processor_count=2)


def initialize_watertight(mesh_session):
    mesh_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")


def reset_workflow(mesh_session):
    mesh_session.workflow.ResetWorkflow()


@pytest.fixture
def new_mesh_session():
    mesher = create_mesh_session()
    yield mesher
    mesher.exit()


@pytest.fixture
def new_watertight_workflow_session(new_mesh_session):
    initialize_watertight(new_mesh_session)
    yield new_mesh_session


@pytest.fixture
def new_watertight_workflow(new_watertight_workflow_session):
    yield new_watertight_workflow_session.workflow


_mesher = None


@pytest.fixture
def shared_mesh_session():
    global _mesher
    if not _mesher:
        _mesher = create_mesh_session()
    return _mesher


@pytest.fixture
def shared_watertight_workflow_session(shared_mesh_session):
    initialize_watertight(shared_mesh_session)
    yield shared_mesh_session
    reset_workflow(shared_mesh_session)


@pytest.fixture
def shared_watertight_workflow(shared_watertight_workflow_session):
    yield shared_watertight_workflow_session.workflow


_mixing_elbow_geometry_file_name = None


@pytest.fixture
def mixing_elbow_geometry():
    global _mixing_elbow_geometry_file_name
    if not _mixing_elbow_geometry_file_name:
        _mixing_elbow_geometry_file_name = download_file(
            file_name="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
        )
    return _mixing_elbow_geometry_file_name


def initialize_fault_tolerant(mesh_session):
    mesh_session.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")


@pytest.fixture
def new_fault_tolerant_workflow_session(new_mesh_session):
    initialize_fault_tolerant(new_mesh_session)
    yield new_mesh_session


@pytest.fixture
def new_fault_tolerant_workflow(new_fault_tolerant_workflow_session):
    yield new_fault_tolerant_workflow_session.workflow


@pytest.fixture
def shared_fault_tolerant_workflow_session(shared_mesh_session):
    initialize_fault_tolerant(shared_mesh_session)
    yield shared_mesh_session
    reset_workflow(shared_mesh_session)


@pytest.fixture
def shared_fault_tolerant_workflow(shared_fault_tolerant_workflow_session):
    yield shared_fault_tolerant_workflow_session.workflow


_exhaust_system_geometry_file_name = None


@pytest.fixture
def exhaust_system_geometry():
    global _exhaust_system_geometry_file_name
    if not _exhaust_system_geometry_file_name:
        _exhaust_system_geometry_file_name = download_file(
            file_name="exhaust_system.fmd", directory="pyfluent/exhaust_system"
        )
    return _exhaust_system_geometry_file_name


"""
@pytest.fixture
def model_object_throws_on_invalid_arg():
    import os
    os.environ["MODEL_OBJECT_THROW_BAD_CHILD"] = "1"
"""
