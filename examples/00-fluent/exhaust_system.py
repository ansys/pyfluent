""".. _ref_exhaust_system_tui_api:

Fault-tolerant meshing workflow
-------------------------------
This example sets up and solves a three-dimensional turbulent fluid flow
in a manifold exhaust system, which is common in the automotive industry.
Predicting the flow field in the area of the mixing region is important
to designing the junction properly.

This example uses the guided workflow for fault-tolerant meshing because it
is appropriate for geometries that can have imperfections, such as gaps and
leakages.

**Workflow tasks**

The fault-tolerant meshing workflow guides you through these tasks:

- Import a CAD geometry and manage individual parts
- Generate a surface mesh
- Cap inlets and outlets
- Extract a fluid region
- Define leakages
- Extract edge features
- Set up size controls
- Generate a volume mesh

**Problem description**

In the manifold exhaust system, air flows through the three inlets
with a uniform velocity of 1 m/s. The air then exits through the outlet.
A small pipe is placed in the main portion of the manifold where edge
extraction is considered. The example also includes a known small leakage
to demonstrate the automatic leakage detection aspects of the meshing workflow.
"""

# sphinx_gallery_thumbnail_path = '_static/exhaust_system.png'

###############################################################################
# Setting up the example
# -----------------------
# Before you can use the fault-tolerant meshing workflow, you must set up the
# example and initialize this workflow.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry file.

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_filename = examples.download_file(
    "exhaust_system.fmd", "pyfluent/exhaust_system"
)

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in meshing mode with double precision running on
# two processors.

session = pyfluent.launch_fluent(
    meshing_mode=True, precision="double", processor_count=2
)

###############################################################################
# Initialize workflow
# ~~~~~~~~~~~~~~~~~~~
# Initialize the fault-tolerant meshing workflow.

session.meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")

###############################################################################
# Using the fault-folerant meshing workflow
# -----------------------------------------
# The fault-tolerant meshing workflow guides you through the several tasks that
# follow.
#
# Import CAD and manage parts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import the CAD geometry (``exhaust_system.fmd``) and selectively manage some
# parts.

session.meshing.PartManagement.InputFileChanged(
    FilePath=import_filename, IgnoreSolidNames=False, PartPerBody=False
)
session.meshing.PMFileManagement.FileManager.LoadFiles()
session.meshing.PartManagement.Node["Meshing Model"].Copy(
    Paths=[
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
    ]
)
session.meshing.PartManagement.ObjectSetting[
    "DefaultObjectSetting"
].OneZonePer.setState("part")
session.meshing.workflow.TaskObject[
    "Import CAD and Part Management"
].Arguments.setState(
    {
        "Context": 0,
        "CreateObjectPer": "Custom",
        "FMDFileName": import_filename,
        "FileLoaded": "yes",
        "ObjectSetting": "DefaultObjectSetting",
        "Options": {
            "Line": False,
            "Solid": False,
            "Surface": False,
        },
    }
)
session.meshing.workflow.TaskObject["Import CAD and Part Management"].Execute()

###############################################################################
# Describe geometry and flow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Describe the geometry and the flow characteristics.

session.meshing.workflow.TaskObject["Describe Geometry and Flow"].Arguments.setState(
    {
        "AddEnclosure": "No",
        "CloseCaps": "Yes",
        "FlowType": "Internal flow through the object",
    }
)
session.meshing.workflow.TaskObject["Describe Geometry and Flow"].UpdateChildTasks(
    SetupTypeChanged=False
)
session.meshing.workflow.TaskObject["Describe Geometry and Flow"].Arguments.setState(
    {
        "AddEnclosure": "No",
        "CloseCaps": "Yes",
        "DescribeGeometryAndFlowOptions": {
            "AdvancedOptions": True,
            "ExtractEdgeFeatures": "Yes",
        },
        "FlowType": "Internal flow through the object",
    }
)
session.meshing.workflow.TaskObject["Describe Geometry and Flow"].UpdateChildTasks(
    SetupTypeChanged=False
)
session.meshing.workflow.TaskObject["Describe Geometry and Flow"].Execute()

###############################################################################
# Enclose openings
# ~~~~~~~~~~~~~~~~
# Enclose (cap) any openings in the geometry.

###############################################################################
# .. image:: /_static/exhaust_system_011.png
#   :width: 400pt
#   :align: center

###############################################################################
# .. image:: /_static/exhaust_system_012.png
#   :width: 400pt
#   :align: center

session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "CreatePatchPreferences": {
            "ShowCreatePatchPreferences": False,
        },
        "PatchName": "inlet-1",
        "SelectionType": "zone",
        "ZoneSelectionList": ["inlet.1"],
    }
)
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "CreatePatchPreferences": {
            "ShowCreatePatchPreferences": False,
        },
        "PatchName": "inlet-1",
        "SelectionType": "zone",
        "ZoneLocation": [
            "1",
            "351.68205",
            "-361.34322",
            "-301.88668",
            "396.96205",
            "-332.84759",
            "-266.69751",
            "inlet.1",
        ],
        "ZoneSelectionList": ["inlet.1"],
    }
)
session.meshing.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].InsertCompoundChildTask()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState({})
session.meshing.workflow.TaskObject["inlet-1"].Execute()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "PatchName": "inlet-2",
        "SelectionType": "zone",
        "ZoneSelectionList": ["inlet.2"],
    }
)
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "PatchName": "inlet-2",
        "SelectionType": "zone",
        "ZoneLocation": [
            "1",
            "441.68205",
            "-361.34322",
            "-301.88668",
            "486.96205",
            "-332.84759",
            "-266.69751",
            "inlet.2",
        ],
        "ZoneSelectionList": ["inlet.2"],
    }
)
session.meshing.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].InsertCompoundChildTask()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState({})
session.meshing.workflow.TaskObject["inlet-2"].Execute()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "PatchName": "inlet-3",
        "SelectionType": "zone",
        "ZoneSelectionList": ["inlet"],
    }
)
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "PatchName": "inlet-3",
        "SelectionType": "zone",
        "ZoneLocation": [
            "1",
            "261.68205",
            "-361.34322",
            "-301.88668",
            "306.96205",
            "-332.84759",
            "-266.69751",
            "inlet",
        ],
        "ZoneSelectionList": ["inlet"],
    }
)
session.meshing.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].InsertCompoundChildTask()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState({})
session.meshing.workflow.TaskObject["inlet-3"].Execute()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "PatchName": "outlet-1",
        "SelectionType": "zone",
        "ZoneSelectionList": ["outlet"],
        "ZoneType": "pressure-outlet",
    }
)
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState(
    {
        "PatchName": "outlet-1",
        "SelectionType": "zone",
        "ZoneLocation": [
            "1",
            "352.22702",
            "-197.8957",
            "84.102381",
            "394.41707",
            "-155.70565",
            "84.102381",
            "outlet",
        ],
        "ZoneSelectionList": ["outlet"],
        "ZoneType": "pressure-outlet",
    }
)
session.meshing.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].InsertCompoundChildTask()
session.meshing.workflow.TaskObject[
    "Enclose Fluid Regions (Capping)"
].Arguments.setState({})
session.meshing.workflow.TaskObject["outlet-1"].Execute()

###############################################################################
# Extract edge features
# ~~~~~~~~~~~~~~~~~~~~~
# Extract edge features.

session.meshing.workflow.TaskObject["Extract Edge Features"].Arguments.setState(
    {
        "ExtractMethodType": "Intersection Loops",
        "ObjectSelectionList": ["flow_pipe", "main"],
    }
)
session.meshing.workflow.TaskObject["Extract Edge Features"].AddChildToTask()

session.meshing.workflow.TaskObject["Extract Edge Features"].InsertCompoundChildTask()

session.meshing.workflow.TaskObject["edge-group-1"].Arguments.setState(
    {
        "ExtractEdgesName": "edge-group-1",
        "ExtractMethodType": "Intersection Loops",
        "ObjectSelectionList": ["flow_pipe", "main"],
    }
)
session.meshing.workflow.TaskObject["Extract Edge Features"].Arguments.setState({})

session.meshing.workflow.TaskObject["edge-group-1"].Execute()

###############################################################################
# Identify regions
# ~~~~~~~~~~~~~~~~
# Identify regions.

session.meshing.workflow.TaskObject["Identify Regions"].Arguments.setState(
    {
        "SelectionType": "zone",
        "X": 377.322045740589,
        "Y": -176.800676988458,
        "Z": -37.0764628583475,
        "ZoneSelectionList": ["main.1"],
    }
)
session.meshing.workflow.TaskObject["Identify Regions"].Arguments.setState(
    {
        "SelectionType": "zone",
        "X": 377.322045740589,
        "Y": -176.800676988458,
        "Z": -37.0764628583475,
        "ZoneLocation": [
            "1",
            "213.32205",
            "-225.28068",
            "-158.25531",
            "541.32205",
            "-128.32068",
            "84.102381",
            "main.1",
        ],
        "ZoneSelectionList": ["main.1"],
    }
)
session.meshing.workflow.TaskObject["Identify Regions"].AddChildToTask()

session.meshing.workflow.TaskObject["Identify Regions"].InsertCompoundChildTask()

session.meshing.workflow.TaskObject["fluid-region-1"].Arguments.setState(
    {
        "MaterialPointsName": "fluid-region-1",
        "SelectionType": "zone",
        "X": 377.322045740589,
        "Y": -176.800676988458,
        "Z": -37.0764628583475,
        "ZoneLocation": [
            "1",
            "213.32205",
            "-225.28068",
            "-158.25531",
            "541.32205",
            "-128.32068",
            "84.102381",
            "main.1",
        ],
        "ZoneSelectionList": ["main.1"],
    }
)
session.meshing.workflow.TaskObject["Identify Regions"].Arguments.setState({})

session.meshing.workflow.TaskObject["fluid-region-1"].Execute()
session.meshing.workflow.TaskObject["Identify Regions"].Arguments.setState(
    {
        "MaterialPointsName": "void-region-1",
        "NewRegionType": "void",
        "ObjectSelectionList": ["inlet-1", "inlet-2", "inlet-3", "main"],
        "X": 374.722045740589,
        "Y": -278.9775145640143,
        "Z": -161.1700719416913,
    }
)
session.meshing.workflow.TaskObject["Identify Regions"].AddChildToTask()

session.meshing.workflow.TaskObject["Identify Regions"].InsertCompoundChildTask()

session.meshing.workflow.TaskObject["Identify Regions"].Arguments.setState({})

session.meshing.workflow.TaskObject["void-region-1"].Execute()

###############################################################################
# Define thresholds for leakages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define thresholds for any potential leakages.

session.meshing.workflow.TaskObject["Define Leakage Threshold"].Arguments.setState(
    {
        "AddChild": "yes",
        "FlipDirection": True,
        "PlaneDirection": "X",
        "RegionSelectionSingle": "void-region-1",
    }
)
session.meshing.workflow.TaskObject["Define Leakage Threshold"].AddChildToTask()

session.meshing.workflow.TaskObject[
    "Define Leakage Threshold"
].InsertCompoundChildTask()
session.meshing.workflow.TaskObject["leakage-1"].Arguments.setState(
    {
        "AddChild": "yes",
        "FlipDirection": True,
        "LeakageName": "leakage-1",
        "PlaneDirection": "X",
        "RegionSelectionSingle": "void-region-1",
    }
)
session.meshing.workflow.TaskObject["Define Leakage Threshold"].Arguments.setState(
    {
        "AddChild": "yes",
    }
)
session.meshing.workflow.TaskObject["leakage-1"].Execute()

###############################################################################
# Review region settings
# ~~~~~~~~~~~~~~~~~~~~~~
# Review the region settings.

session.meshing.workflow.TaskObject["Update Region Settings"].Arguments.setState(
    {
        "AllRegionFilterCategories": ["2"] * 5 + ["1"] * 2,
        "AllRegionLeakageSizeList": ["none"] * 6 + ["6.4"],
        "AllRegionLinkedConstructionSurfaceList": ["n/a"] * 6 + ["no"],
        "AllRegionMeshMethodList": ["none"] * 6 + ["wrap"],
        "AllRegionNameList": [
            "main",
            "flow_pipe",
            "outpipe3",
            "object2",
            "object1",
            "void-region-1",
            "fluid-region-1",
        ],
        "AllRegionOversetComponenList": ["no"] * 7,
        "AllRegionSourceList": ["object"] * 5 + ["mpt"] * 2,
        "AllRegionTypeList": ["void"] * 6 + ["fluid"],
        "AllRegionVolumeFillList": ["none"] * 6 + ["tet"],
        "FilterCategory": "Identified Regions",
        "OldRegionLeakageSizeList": [""],
        "OldRegionMeshMethodList": ["wrap"],
        "OldRegionNameList": ["fluid-region-1"],
        "OldRegionOversetComponenList": ["no"],
        "OldRegionTypeList": ["fluid"],
        "OldRegionVolumeFillList": ["hexcore"],
        "RegionLeakageSizeList": [""],
        "RegionMeshMethodList": ["wrap"],
        "RegionNameList": ["fluid-region-1"],
        "RegionOversetComponenList": ["no"],
        "RegionTypeList": ["fluid"],
        "RegionVolumeFillList": ["tet"],
    }
)
session.meshing.workflow.TaskObject["Update Region Settings"].Execute()


###############################################################################
# Set mesh control options
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Set options for controlling the mesh.

session.meshing.workflow.TaskObject["Choose Mesh Control Options"].Execute()

###############################################################################
# Generate surface mesh
# ~~~~~~~~~~~~~~~~~~~~~
# Generate the surface mesh.

###############################################################################
# .. image:: /_static/exhaust_system_013.png
#   :width: 500pt
#   :align: center

session.meshing.workflow.TaskObject["Generate the Surface Mesh"].Execute()

###############################################################################
# Confirm and update boundaries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Confirm and update the boundaries.

session.meshing.workflow.TaskObject["Update Boundaries"].Execute()

###############################################################################
# Add boundary layers
# ~~~~~~~~~~~~~~~~~~~
# Add boundary layers.

session.meshing.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()

session.meshing.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()

session.meshing.workflow.TaskObject["aspect-ratio_1"].Arguments.setState(
    {
        "BLControlName": "aspect-ratio_1",
    }
)
session.meshing.workflow.TaskObject["Add Boundary Layers"].Arguments.setState({})

session.meshing.workflow.TaskObject["aspect-ratio_1"].Execute()

###############################################################################
# Generate volume mesh
# ~~~~~~~~~~~~~~~~~~~~
# Generate the volume mesh.

###############################################################################
# .. image:: /_static/exhaust_system_014.png
#   :width: 500pt
#   :align: center

session.meshing.workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
    {
        "AllRegionNameList": [
            "main",
            "flow_pipe",
            "outpipe3",
            "object2",
            "object1",
            "void-region-1",
            "fluid-region-1",
        ],
        "AllRegionSizeList": ["11.33375"] * 7,
        "AllRegionVolumeFillList": ["none"] * 6 + ["tet"],
        "EnableParallel": True,
    }
)
session.meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()

###############################################################################
# Check mesh
# ~~~~~~~~~~
# Check the mesh.

session.meshing.tui.mesh.check_mesh()

###############################################################################
# Solve and Postprocess
# ----------------------
# Once you have completed the fault tolerate meshing workflow, you can solve and
# postprcess the results.
#
# Switch to solution mode
# ~~~~~~~~~~~~~~~~~~~~~~~
# Switch to the solution mode.

session.meshing.tui.switch_to_solution_mode("yes")

session.solver.tui.mesh.check()

###############################################################################
# Set units for length
# ~~~~~~~~~~~~~~~~~~~~
# Set the units for length.

session.solver.tui.define.units("length", "mm")

###############################################################################
# Select turbulence model
# ~~~~~~~~~~~~~~~~~~~~~~~
# Select the kw sst turbulence model.

session.solver.tui.define.models.viscous.kw_sst("yes")

###############################################################################
# Set velocity and turbulence boundary conditions for first inlet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the velocity and turbulence boundary conditions for the first inlet
# (inlet-1).

session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet-1", [], "vmag", "no", 1, "quit"
)

###############################################################################
# Set same boundary conditions for other velocity inlets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the same boundary conditions for the other velocity inlets (inlet_2
# and inlet_3).

session.solver.tui.define.boundary_conditions.copy_bc(
    "inlet-1", "inlet-2", "inlet-3", ()
)

###############################################################################
# Set boundary conditions at outlet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the boundary conditions at the outlet (outlet-1).

session.solver.tui.define.boundary_conditions.set.pressure_outlet(
    "outlet-1", [], "turb-intensity", 5, "quit"
)
session.solver.tui.solve.monitors.residual.plot("yes")

###############################################################################
# Initialize flow field
# ~~~~~~~~~~~~~~~~~~~~~
# Initialize the flow field using the hybrid initialization.

session.solver.tui.solve.initialize.hyb_initialization()

###############################################################################
# Start calculation
# ~~~~~~~~~~~~~~~~~
# Start the calculation by requesting 100 iterations.

###############################################################################
# .. image:: /_static/exhaust_system_015.png
#   :width: 500pt
#   :align: center

session.solver.tui.solve.set.number_of_iterations(100)
session.solver.tui.solve.iterate()

# session.solver.tui.report.volume_integrals.volume("fluid-region-1","()","yes","volume.vrp")

###############################################################################
# Create path lines
# ~~~~~~~~~~~~~~~~~
# Create path lines highlighting the flow field.

###############################################################################
# .. image:: /_static/exhaust_system_016.png
#   :width: 500pt
#   :align: center

session.solver.tui.display.objects.create(
    "pathlines",
    "pathlines-1",
    "field",
    "time",
    "accuracy-control",
    "tolerance",
    "0.001",
    "skip",
    "5",
    "surfaces-list",
    "inlet-1",
    "inlet-2",
    "inlet-3",
    "()",
    "quit",
)

###############################################################################
# Create iso-surface
# ~~~~~~~~~~~~~~~~~~
# Create an iso-surface through the manifold geometry.

session.solver.tui.surface.iso_surface(
    "x-coordinate",
    "surf-x-coordinate",
    "()",
    "fluid-region-1",
    "()",
    "380",
    "()",
)

###############################################################################
# Create contours of velocity magnitude
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create contours of the velocity magnitude throughout the manifold
# along with the mesh.

###############################################################################
# .. image:: /_static/exhaust_system_017.png
#   :width: 500pt
#   :align: center

session.solver.tui.display.objects.create(
    "contour",
    "contour-velocity",
    "field",
    "velocity-magnitude",
    "surfaces-list",
    "surf-x-coordinate",
    "()",
    "node-values?",
    "no",
    "range-option",
    "auto-range-on",
    "global-range?",
    "no",
    "quit",
    "quit",
)

session.solver.tui.display.objects.create(
    "mesh", "mesh-1", "surfaces-list", "*", "()", "quit"
)

###############################################################################
# Create scene
# ~~~~~~~~~~~~
# Create a scene containing the mesh and the contours.

###############################################################################
# .. image:: /_static/exhaust_system_018.png
#   :width: 500pt
#   :align: center

session.solver.tui.display.objects.create(
    "scene",
    "scene-1",
    "graphics-objects",
    "add",
    "mesh-1",
    "transparency",
    "90",
    "quit",
    "add",
    "contour-velocity",
    "quit",
    "quit",
    "quit",
)

#########################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

session.exit()
