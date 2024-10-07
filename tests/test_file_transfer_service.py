"""Test file transfer service."""

import os
import pathlib

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.utils.file_transfer_service import (
    LocalFileTransferStrategy,
    RemoteFileTransferStrategy,
)


def file_downloaded_to_the_client(file_name: str) -> bool:
    """Check if client file exists.

    Parameters
    ----------
    file_name: str
        File name.

    Returns
    -------
        Whether file exists.
    """
    full_file_name = pathlib.Path(
        "/home/runner/.local/share/ansys_fluent_core/examples"
    ) / os.path.basename(file_name)
    return full_file_name.is_file()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.2")
def test_remote_grpc_fts_container(
    monkeypatch, new_solver_session, new_meshing_session
):
    solver = new_solver_session
    import_case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    import_mesh_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read_case(file_name=import_case_file_name)
    if solver._file_transfer_service:
        solver.file.write_case(file_name="downloaded_solver_mixing_elbow.cas.h5")
        assert solver.file_exists_on_remote("downloaded_solver_mixing_elbow.cas.h5")
        assert file_downloaded_to_the_client("downloaded_solver_mixing_elbow.cas.h5")

    meshing = new_meshing_session
    meshing.meshing.File.ReadMesh(FileName=import_mesh_file_name)
    if meshing._file_transfer_service:
        meshing.meshing.File.WriteMesh(
            FileName="downloaded_meshing_mixing_elbow.msh.h5"
        )
        assert meshing.file_exists_on_remote("downloaded_meshing_mixing_elbow.msh.h5")
        assert file_downloaded_to_the_client("downloaded_meshing_mixing_elbow.msh.h5")


@pytest.mark.standalone
def test_read_case_and_data(monkeypatch):
    import ansys.fluent.core as pyfluent

    monkeypatch.setattr(pyfluent, "USE_FILE_TRANSFER_SERVICE", True)

    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    data_file_name = examples.download_file(
        "mixing_elbow.dat.h5", "pyfluent/mixing_elbow"
    )
    assert case_file_name
    assert data_file_name
    solver = pyfluent.launch_fluent(file_transfer_service=LocalFileTransferStrategy())

    solver.file.read(file_type="case-data", file_name=case_file_name)
    solver.file.write(file_type="case-data", file_name="write_data.cas.h5")

    solver.file.read_case_data(file_name=case_file_name)
    solver.file.write_case_data(file_name="write_case_data.cas.h5")
    solver.exit()

    solver = pyfluent.launch_fluent(
        file_transfer_service=LocalFileTransferStrategy(server_cwd=os.getcwd())
    )

    solver.file.read(file_type="case-data", file_name=case_file_name)
    solver.file.write(file_type="case-data", file_name="write_data.cas.h5")

    solver.file.read_case_data(file_name=case_file_name)
    solver.file.write_case_data(file_name="write_case_data.cas.h5")
    solver.exit()


@pytest.mark.skip(reason="Skips upload even after adding ImportGeometry task object.")
def test_datamodel_execute():
    import ansys.fluent.core as pyfluent

    meshing = pyfluent.launch_fluent(
        mode="meshing", file_transfer_service=RemoteFileTransferStrategy()
    )
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_geom = meshing.workflow.TaskObject["Import Geometry"]
    import_geom.Arguments = {"FileName": "geom"}

    with pytest.raises(RuntimeError):
        import_geom.Execute()


def test_file_list_in_datamodel(fault_tolerant_workflow_session):
    meshing = fault_tolerant_workflow_session
    fmd_file = examples.download_file("exhaust_system.fmd", "pyfluent/exhaust_system")
    meshing.PartManagement.AppendFmdFiles(
        AssemblyParentNode=0,
        FilePath=[fmd_file],
        FileUnit="mm",
        IgnoreSolidNamesAppend=False,
        JtLOD="1",
        Options={
            "Line": False,
            "Solid": True,
            "Surface": True,
        },
        PartPerBody=False,
        PrefixParentName=False,
        RemoveEmptyParts=True,
        Route="Native",
    )


@pytest.mark.standalone
def test_local_file_transfer_in_datamodel(monkeypatch):
    import ansys.fluent.core as pyfluent

    monkeypatch.setattr(pyfluent, "USE_FILE_TRANSFER_SERVICE", True)

    fmd_file = examples.download_file("exhaust_system.fmd", "pyfluent/exhaust_system")

    assert fmd_file

    meshing = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING,
        file_transfer_service=LocalFileTransferStrategy(),
    )

    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")

    meshing.PartManagement.AppendFmdFiles(
        AssemblyParentNode=0,
        FilePath=[fmd_file],
        FileUnit="mm",
        IgnoreSolidNamesAppend=False,
        JtLOD="1",
        Options={
            "Line": False,
            "Solid": True,
            "Surface": True,
        },
        PartPerBody=False,
        PrefixParentName=False,
        RemoveEmptyParts=True,
        Route="Native",
    )
    meshing.exit()
