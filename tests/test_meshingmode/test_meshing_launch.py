import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.nightly
@pytest.mark.mesh
@pytest.mark.fluent_version("dev")
@pytest.mark.codegen_required
def test_launch_pure_meshing(load_mixing_elbow_pure_meshing):
    pure_meshing_session = load_mixing_elbow_pure_meshing
    assert pure_meshing_session.health_check_service.is_serving
    file_path = "launch_pure_meshing_journal.py"
    pure_meshing_session.journal.start(file_path)
    session_dir = dir(pure_meshing_session)
    for attr in ("field_data", "field_info", "meshing", "workflow"):
        assert attr in session_dir
    workflow = pure_meshing_session.workflow
    workflow.TaskObject["Import Geometry"].Execute()
    workflow.TaskObject["Add Local Sizing"].AddChildToTask()
    workflow.TaskObject["Add Local Sizing"].Execute()
    workflow.TaskObject["Generate the Surface Mesh"].Arguments = {
        "CFDSurfaceMeshControls": {"MaxSize": 0.3}
    }
    workflow.TaskObject["Generate the Surface Mesh"].Execute()
    workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=False)
    workflow.TaskObject["Describe Geometry"].Arguments = dict(
        SetupType="The geometry consists of only fluid regions with no voids"
    )
    workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=True)
    workflow.TaskObject["Describe Geometry"].Execute()
    workflow.TaskObject["Update Boundaries"].Arguments = {
        "BoundaryLabelList": ["wall-inlet"],
        "BoundaryLabelTypeList": ["wall"],
        "OldBoundaryLabelList": ["wall-inlet"],
        "OldBoundaryLabelTypeList": ["velocity-inlet"],
    }
    workflow.TaskObject["Update Boundaries"].Execute()
    workflow.TaskObject["Update Regions"].Execute()
    workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
    workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
    workflow.TaskObject["smooth-transition_1"].Arguments = {
        "BLControlName": "smooth-transition_1",
    }
    workflow.TaskObject["Add Boundary Layers"].Arguments = {}
    workflow.TaskObject["smooth-transition_1"].Execute()
    workflow.TaskObject["Generate the Volume Mesh"].Arguments = {
        "VolumeFill": "poly-hexcore",
        "VolumeFillControls": {
            "HexMaxCellLength": 0.3,
        },
    }
    workflow.TaskObject["Generate the Volume Mesh"].Execute()
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
    pure_meshing_session.tui.file.read_journal(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
