import pytest

import ansys.fluent.core as pyfluent


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
    if task_name not in ("Add Local Sizing", "Add Boundary Layers"):
        assert result is True
    check_task_execute_postconditions(task)


_mesher = None


@pytest.fixture
def mesh_session():
    global _mesher
    if not _mesher:
        _mesher = pyfluent.launch_fluent(
            meshing_mode=True, precision="double", processor_count=2
        )
    return _mesher


@pytest.fixture
def watertight_workflow_session(mesh_session):
    mesh_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    yield mesh_session
    mesh_session.workflow.ResetWorkflow()


@pytest.fixture
def watertight_workflow(watertight_workflow_session):
    return watertight_workflow_session.workflow
