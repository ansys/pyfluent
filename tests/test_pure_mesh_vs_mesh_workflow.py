import pytest

from ansys.fluent.core.examples import download_file


def test_pure_meshing_mode(load_mixing_elbow_pure_meshing):
    pure_meshing_session = load_mixing_elbow_pure_meshing
    # check a few dir elements
    # n.b. 'field_data', 'field_info' need to
    # be eliminated from meshing sessions
    session_dir = dir(pure_meshing_session)
    for attr in ("field_data", "field_info", "meshing", "workflow"):
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


def test_meshing_mode(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    # check a few dir elements
    # n.b. 'field_data', 'field_info' need to
    # be eliminated from meshing sessions
    session_dir = dir(meshing_session)
    for attr in ("field_data", "field_info", "meshing", "workflow"):
        assert attr in session_dir
    assert meshing_session.workflow.InitializeWorkflow(
        WorkflowType="Watertight Geometry"
    )
    assert meshing_session.switch_to_solver()


def test_meshing_and_solver_mode_exit(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    solver_session = meshing_session.switch_to_solver()
    # Even if exit statement is invoked twice, only one is executed as the channel instance is shared
    meshing_session.exit()
    solver_session.exit()


def test_meshing_mode_post_switching_to_solver(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    meshing_session.switch_to_solver()
    # Post switching to solver session, meshing session specific attributes are unavailable
    with pytest.raises(AttributeError):
        meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")


# def test_transfer_mesh_to_solvers(
#     launch_fluent_pure_meshing, launch_fluent_solver_3ddp_t2
# ):
#     mesh_filename = download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
#     pure_meshing_session = launch_fluent_pure_meshing
#     pure_meshing_session.tui.file.read_mesh(mesh_filename)
#     pure_meshing_session.tui.mesh.check_mesh()
#     mesh_info = pure_meshing_session.scheme_eval.string_eval(
#         "(%tg-length-of-entity-list)"
#     )
#     pure_meshing_session_cell_count = mesh_info.strip("( )").split()[3]
#
#     solver_session = launch_fluent_solver_3ddp_t2
#     pure_meshing_session.transfer_mesh_to_solvers([solver_session], file_type="mesh")
#     solver_session.tui.mesh.check()
#     mesh_info = solver_session.scheme_eval.string_eval("(inquire-grids)")
#     solver_session_cell_count = mesh_info.strip("( )").split()[1]
#
#     assert pure_meshing_session_cell_count == solver_session_cell_count


def test_transfer_case_to_solvers(
    launch_fluent_pure_meshing, launch_fluent_solver_3ddp_t2
):
    case_filename = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    pure_meshing_session = launch_fluent_pure_meshing
    pure_meshing_session.tui.file.read_case(case_filename)
    pure_meshing_session.tui.mesh.check_mesh()
    mesh_info = pure_meshing_session.scheme_eval.string_eval(
        "(%tg-length-of-entity-list)"
    )
    pure_meshing_session_cell_count = mesh_info.strip("( )").split()[3]

    solver_session = launch_fluent_solver_3ddp_t2
    pure_meshing_session.transfer_mesh_to_solvers([solver_session], file_type="case")
    solver_session.tui.mesh.check()
    mesh_info = solver_session.scheme_eval.string_eval("(inquire-grids)")
    solver_session_cell_count = mesh_info.strip("( )").split()[1]

    assert pure_meshing_session_cell_count == solver_session_cell_count
