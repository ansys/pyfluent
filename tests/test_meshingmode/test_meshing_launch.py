import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.nightly
@pytest.mark.fluent_version("latest")
@pytest.mark.codegen_required
def test_launch_pure_meshing(load_mixing_elbow_pure_meshing):
    pure_meshing_session = load_mixing_elbow_pure_meshing
    assert pure_meshing_session.health_check_service.is_serving
    file_name = "launch_pure_meshing_journal.py"
    pure_meshing_session.journal.start(file_name)
    session_dir = dir(pure_meshing_session)
    for attr in ("field_data", "field_info", "meshing", "workflow"):
        assert attr in session_dir
    workflow = pure_meshing_session.workflow
    workflow.TaskObject["Import Geometry"].Execute()

    add_local_sizing = workflow.TaskObject["Add Local Sizing"]
    add_local_sizing.AddChildToTask()
    add_local_sizing.Execute()

    surface_mesh_gen = workflow.TaskObject["Generate the Surface Mesh"]
    surface_mesh_gen.Arguments = {"CFDSurfaceMeshControls": {"MaxSize": 0.3}}
    surface_mesh_gen.Execute()

    describe_geo = workflow.TaskObject["Describe Geometry"]
    describe_geo.UpdateChildTasks(SetupTypeChanged=False)
    describe_geo.Arguments = dict(
        SetupType="The geometry consists of only fluid regions with no voids"
    )
    describe_geo.UpdateChildTasks(SetupTypeChanged=True)
    describe_geo.Execute()

    boundary_update = workflow.TaskObject["Update Boundaries"]
    boundary_update.Arguments = {
        "BoundaryLabelList": ["wall-inlet"],
        "BoundaryLabelTypeList": ["wall"],
        "OldBoundaryLabelList": ["wall-inlet"],
        "OldBoundaryLabelTypeList": ["velocity-inlet"],
    }
    boundary_update.Execute()

    workflow.TaskObject["Update Regions"].Execute()

    add_boundary_layers = workflow.TaskObject["Add Boundary Layers"]
    add_boundary_layers.AddChildToTask()
    add_boundary_layers.InsertCompoundChildTask()
    smooth_transition_1 = workflow.TaskObject["smooth-transition_1"]
    smooth_transition_1.Arguments = {
        "BLControlName": "smooth-transition_1",
    }
    add_boundary_layers.Arguments = {}
    smooth_transition_1.Execute()
    volume_mesh_gen = workflow.TaskObject["Generate the Volume Mesh"]
    volume_mesh_gen.Arguments = {
        "VolumeFill": "poly-hexcore",
        "VolumeFillControls": {
            "HexMaxCellLength": 0.3,
        },
    }
    volume_mesh_gen.Execute()

    pure_meshing_session.journal.stop()
    with pytest.raises(AttributeError):
        pure_meshing_session.switch_to_solver()
    pure_meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    input_type, input_name = download_input_file(
        "pyfluent/mixing_elbow", "mixing_elbow.pmdb"
    )
    pure_meshing_session.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=input_name, LengthUnit="in"
    )
    pure_meshing_session.tui.file.read_journal(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)
