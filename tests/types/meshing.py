from collections.abc import Callable
from typing import cast

from typing_extensions import assert_type

import ansys.fluent.core as pyfluent
from ansys.fluent.core.meshing import meshing_workflow as mesh_wf_old
from ansys.fluent.core.meshing import meshing_workflow_new as mesh_wf_new
from ansys.fluent.core.meshing.meshing_workflow_new import WatertightMeshingWorkflow
from ansys.fluent.core.session_meshing import Meshing

meshing = cast(Meshing, pyfluent.Meshing.from_install())

# watertight tests
assert_type(meshing.watertight(legacy=True), mesh_wf_old.WatertightMeshingWorkflow)
assert_type(meshing.watertight(legacy=False), WatertightMeshingWorkflow)
assert_type(
    meshing.watertight(),
    mesh_wf_new.WatertightMeshingWorkflow | mesh_wf_old.WatertightMeshingWorkflow,
)
assert_type(
    meshing.watertight(legacy=False).application, WatertightMeshingWorkflow._application
)
assert_type(
    meshing.watertight(legacy=False).application.set_state, Callable[..., None]
)  # still has base class attributes

# local_sizing exists on both
watertight_new = meshing.watertight(legacy=False)
assert_type(
    watertight_new.application.add_local_sizing_wtm,
    mesh_wf_new._application._add_local_sizing_wtm,
)
watertight_legacy = meshing.watertight(legacy=True)
assert_type(watertight_legacy.add_local_sizing, mesh_wf_old.BaseTask)

# fault_tolerant tests
assert_type(
    meshing.fault_tolerant(legacy=True), mesh_wf_old.FaultTolerantMeshingWorkflow
)
assert_type(
    meshing.fault_tolerant(legacy=False), mesh_wf_new.FaultTolerantMeshingWorkflow
)
assert_type(
    meshing.fault_tolerant(),
    mesh_wf_new.FaultTolerantMeshingWorkflow | mesh_wf_old.FaultTolerantMeshingWorkflow,
)

# two_dimensional_meshing tests  # TODO would be nice to only have this if Meshing[DimT=Literal[2D]]
assert_type(
    meshing.two_dimensional_meshing(legacy=True),
    mesh_wf_old.TwoDimensionalMeshingWorkflow,
)
assert_type(
    meshing.two_dimensional_meshing(legacy=False),
    mesh_wf_new.TwoDimensionalMeshingWorkflow,
)
assert_type(
    meshing.two_dimensional_meshing(),
    mesh_wf_new.TwoDimensionalMeshingWorkflow
    | mesh_wf_old.TwoDimensionalMeshingWorkflow,
)

# load_workflow tests
assert_type(meshing.load_workflow("test.wft", legacy=True), mesh_wf_old.Workflow)
assert_type(meshing.load_workflow("test.wft", legacy=False), mesh_wf_new.Workflow)
assert_type(
    meshing.load_workflow("test.wft"), mesh_wf_new.Workflow | mesh_wf_old.Workflow
)

# create_workflow tests
assert_type(meshing.create_workflow(legacy=True), mesh_wf_old.Workflow)
assert_type(meshing.create_workflow(legacy=False), mesh_wf_new.Workflow)
assert_type(meshing.create_workflow(), mesh_wf_new.Workflow | mesh_wf_old.Workflow)

# topology_based tests
assert_type(meshing.topology_based(legacy=True), mesh_wf_old.Workflow)
assert_type(meshing.topology_based(legacy=False), mesh_wf_new.Workflow)
assert_type(meshing.topology_based(), mesh_wf_new.Workflow | mesh_wf_old.Workflow)
