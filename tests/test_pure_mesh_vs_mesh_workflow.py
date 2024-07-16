import pytest

from ansys.fluent.core.examples import download_file


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.1")
def test_pure_meshing_mode(mixing_elbow_watertight_pure_meshing_session):
    pure_meshing_session = mixing_elbow_watertight_pure_meshing_session
    # check a few dir elements
    # n.b. 'field_data', 'field_info' need to
    # be eliminated from meshing sessions
    session_dir = dir(pure_meshing_session)
    for attr in ("fields", "meshing", "workflow"):
        assert attr in session_dir
    workflow = pure_meshing_session.workflow
    workflow_dir = dir(workflow)
    for attr in ("TaskObject", "InsertNewTask", "Workflow", "setState"):
        assert attr in workflow_dir
    import_geometry = workflow.TaskObject["Import Geometry"]
    import_geometry_dir = dir(import_geometry)
    for attr in ("AddChildToTask", "Arguments", "Execute", "setState"):
        assert attr in import_geometry_dir
    with pytest.raises(AttributeError):
        pure_meshing_session.switch_to_solver()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.1")
def test_meshing_mode(new_meshing_session):
    meshing_session = new_meshing_session
    # check a few dir elements
    # n.b. 'field_data', 'field_info' need to
    # be eliminated from meshing sessions
    session_dir = dir(meshing_session)
    for attr in ("fields", "meshing", "workflow"):
        assert attr in session_dir
    assert meshing_session.workflow.InitializeWorkflow(
        WorkflowType="Watertight Geometry"
    )
    assert meshing_session.switch_to_solver()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.1")
def test_meshing_and_solver_mode_exit(new_meshing_session):
    meshing_session = new_meshing_session
    solver_session = meshing_session.switch_to_solver()
    # Even if exit statement is invoked twice, only one is executed as the channel instance is shared
    meshing_session.exit()
    solver_session.exit()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.1")
def test_meshing_mode_post_switching_to_solver(new_meshing_session):
    meshing_session = new_meshing_session
    meshing_session.switch_to_solver()
    # Post switching to solver session, meshing session specific attributes are unavailable
    with pytest.raises(AttributeError):
        meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")


# def test_transfer_mesh_to_solvers(
#     new_pure_meshing_session, new_solver_session
# ):
#     mesh_file_name = download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
#     pure_meshing_session = new_pure_meshing_session
#     pure_meshing_session.tui.file.read_mesh(mesh_file_name)
#     pure_meshing_session.tui.mesh.check_mesh()
#     mesh_info = pure_meshing_session.scheme_eval.string_eval(
#         "(%tg-length-of-entity-list)"
#     )
#     pure_meshing_session_cell_count = mesh_info.strip("( )").split()[3]
#
#     solver_session = new_solver_session
#     pure_meshing_session.transfer_mesh_to_solvers([solver_session], file_type="mesh")
#     solver_session.tui.mesh.check()
#     mesh_info = solver_session.scheme_eval.string_eval("(inquire-grids)")
#     solver_session_cell_count = mesh_info.strip("( )").split()[1]
#
#     assert pure_meshing_session_cell_count == solver_session_cell_count


def test_transfer_case_to_solvers(new_pure_meshing_session, new_solver_session):
    case_file_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    pure_meshing_session = new_pure_meshing_session
    pure_meshing_session.tui.file.read_case(case_file_name)
    pure_meshing_session.tui.mesh.check_mesh()
    mesh_info = pure_meshing_session.scheme_eval.string_eval(
        "(%tg-length-of-entity-list)"
    )
    pure_meshing_session_cell_count = mesh_info.strip("( )").split()[3]

    solver_session = new_solver_session
    pure_meshing_session.transfer_mesh_to_solvers([solver_session], file_type="case")
    solver_session.tui.mesh.check()
    mesh_info = solver_session.scheme_eval.string_eval("(inquire-grids)")
    solver_session_cell_count = mesh_info.strip("( )").split()[1]

    assert pure_meshing_session_cell_count == solver_session_cell_count
