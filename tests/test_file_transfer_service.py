# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test file transfer service."""

import os
from pathlib import Path

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.utils.file_transfer_service import (
    ContainerFileTransferStrategy,
    StandaloneFileTransferStrategy,
)


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.2")
def test_remote_grpc_fts_container():
    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples
    from ansys.fluent.core.utils.file_transfer_service import (
        ContainerFileTransferStrategy,
    )

    case_file = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow", return_without_path=False
    )

    source_path = Path.home() / "Downloads" / "ansys_fluent_core_examples"
    if not source_path.exists():
        source_path.mkdir(parents=True, exist_ok=True)

    file_transfer_service = ContainerFileTransferStrategy(mount_source=str(source_path))

    container_dict = {"mount_source": file_transfer_service.mount_source}
    session = pyfluent.launch_fluent(
        file_transfer_service=file_transfer_service, container_dict=container_dict
    )

    session.file.read_case(file_name=case_file)
    assert session.file_exists_on_remote("mixing_elbow.cas.h5")

    session.file.write_case(file_name="write_mixing_elbow.cas.h5")
    assert session.file_exists_on_remote("write_mixing_elbow.cas.h5")

    session.exit()


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
    solver = pyfluent.launch_fluent(
        file_transfer_service=StandaloneFileTransferStrategy()
    )

    solver.file.read(file_type="case-data", file_name=case_file_name)
    solver.file.write(file_type="case-data", file_name="write_data.cas.h5")

    solver.file.read_case_data(file_name=case_file_name)
    solver.file.write_case_data(file_name="write_case_data.cas.h5")
    solver.exit()

    solver = pyfluent.launch_fluent(
        file_transfer_service=StandaloneFileTransferStrategy(server_cwd=os.getcwd())
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
        mode="meshing", file_transfer_service=ContainerFileTransferStrategy()
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
        file_transfer_service=StandaloneFileTransferStrategy(),
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
