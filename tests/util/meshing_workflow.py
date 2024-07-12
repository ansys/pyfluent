import pytest


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


def initialize_watertight(mesh_session):
    mesh_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")


def reset_workflow(mesh_session):
    mesh_session.workflow.ResetWorkflow()


def initialize_fault_tolerant(mesh_session):
    mesh_session.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")


@pytest.fixture
def new_fault_tolerant_workflow_session(new_meshing_session):
    initialize_fault_tolerant(new_meshing_session)
    yield new_meshing_session


@pytest.fixture
def new_fault_tolerant_workflow(new_fault_tolerant_workflow_session):
    yield new_fault_tolerant_workflow_session.workflow


_exhaust_system_geometry_file_name = None


"""
@pytest.fixture
def model_object_throws_on_invalid_arg():
    import os
    os.environ["MODEL_OBJECT_THROW_BAD_CHILD"] = "1"
"""
