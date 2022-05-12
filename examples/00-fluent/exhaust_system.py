""".. _ref_exhaust_system_tui_api:

Exhaust System: Fault-tolerant Meshing
----------------------------------------------

This tutorial illustrates the setup and solution of a three-dimensional
turbulent fluid flow in a manifold exhaust system. The manifold configuration
is encountered in the automotive industry. It is often important to predict
the flow field in the area of the mixing region in order to properly design
the junction. You will use the Fault-tolerant Meshing guided workflow, which
unlike the watertight workflow used in Fluid Flow in a Mixing Elbow, is
appropriate for geometries with imperfections, such as gaps and leakages.

This tutorial demonstrates how to do the following in Ansys Fluent:


- Use the Fault-tolerant Meshing guided workflow to:
    - Import a CAD geometry and manage individual parts
    - Generate a surface mesh
    - Cap inlets and outlets
    - Extract a fluid region
    - Define leakages
    - Extract edge features
    - Setup size controls
    - Generate a volume mesh
- Set up appropriate physics and boundary conditions.
- Calculate a solution.
- Review the results of the simulation.

Problem Description:

Air flows through the three inlets with a uniform velocity of 1 m/s, and then
exits through the outlet. A small pipe is placed in the main portion of the
manifold where edge extraction will be considered. There is also a known small
leakage included that will be addressed in the meshing portion of the tutorial
to demonstrate the automatic leakage detection aspects of the meshing workflow.
"""

###############################################################################
# First, connect with a Fluent server

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_filename = examples.download_file(
    "exhaust_system.fmd", "pyfluent/exhaust_system"
)

###############################################################################
# Start Fluent in double precision running on 2 processors

session = pyfluent.launch_fluent(
    meshing_mode=True, precision="double", processor_count=4
)

###############################################################################
# Select the Fault Tolerant Meshing Workflow

session.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")

###############################################################################
# Import the CAD geometry (exhaust_system.fmd). Perform some selective part
# management.

session.part_management.InputFileChanged(
    FilePath=import_filename, IgnoreSolidNames=False, PartPerBody=False
)
session.PMFileManagement.FileManager.LoadFiles()
session.part_management.Node["Meshing Model"].Copy(
    Paths=[
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
        "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
    ]
)
session.part_management.ObjectSetting["DefaultObjectSetting"].OneZonePer.setState(
    "part"
)
session.workflow.TaskObject["Import CAD and Part Management"].Arguments.setState(
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
session.workflow.TaskObject["Import CAD and Part Management"].Execute()

###############################################################################
# Provide a description for the geometry and the flow characteristics.

session.workflow.TaskObject["Describe Geometry and Flow"].Arguments.setState(
    {
        "AddEnclosure": "No",
        "CloseCaps": "Yes",
        "FlowType": "Internal flow through the object",
    }
)
session.workflow.TaskObject["Describe Geometry and Flow"].UpdateChildTasks(
    SetupTypeChanged=False
)
session.workflow.TaskObject["Describe Geometry and Flow"].Arguments.setState(
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
session.workflow.TaskObject["Describe Geometry and Flow"].UpdateChildTasks(
    SetupTypeChanged=False
)
session.workflow.TaskObject["Describe Geometry and Flow"].Execute()

###############################################################################
# Cover any openings in your geometry.

session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
    {
        "CreatePatchPreferences": {
            "ShowCreatePatchPreferences": False,
        },
        "PatchName": "inlet-1",
        "SelectionType": "zone",
        "ZoneSelectionList": ["inlet.1"],
    }
)
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
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
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].InsertCompoundChildTask()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState({})
session.workflow.TaskObject["inlet-1"].Execute()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
    {
        "PatchName": "inlet-2",
        "SelectionType": "zone",
        "ZoneSelectionList": ["inlet.2"],
    }
)
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
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
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].InsertCompoundChildTask()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState({})
session.workflow.TaskObject["inlet-2"].Execute()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
    {
        "PatchName": "inlet-3",
        "SelectionType": "zone",
        "ZoneSelectionList": ["inlet"],
    }
)
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
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
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].InsertCompoundChildTask()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState({})
session.workflow.TaskObject["inlet-3"].Execute()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
    {
        "PatchName": "outlet-1",
        "SelectionType": "zone",
        "ZoneSelectionList": ["outlet"],
        "ZoneType": "pressure-outlet",
    }
)
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState(
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
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].AddChildToTask()

session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].InsertCompoundChildTask()
session.workflow.TaskObject["Enclose Fluid Regions (Capping)"].Arguments.setState({})
session.workflow.TaskObject["outlet-1"].Execute()

###############################################################################
# Extract edge features.

session.workflow.TaskObject["Extract Edge Features"].Arguments.setState(
    {
        "ExtractMethodType": "Intersection Loops",
        "ObjectSelectionList": ["flow_pipe", "main"],
    }
)
session.workflow.TaskObject["Extract Edge Features"].AddChildToTask()

session.workflow.TaskObject["Extract Edge Features"].InsertCompoundChildTask()

session.workflow.TaskObject["edge-group-1"].Arguments.setState(
    {
        "ExtractEdgesName": "edge-group-1",
        "ExtractMethodType": "Intersection Loops",
        "ObjectSelectionList": ["flow_pipe", "main"],
    }
)
session.workflow.TaskObject["Extract Edge Features"].Arguments.setState({})

session.workflow.TaskObject["edge-group-1"].Execute()

###############################################################################
# Identify regions.

session.workflow.TaskObject["Identify Regions"].Arguments.setState(
    {
        "SelectionType": "zone",
        "X": 377.322045740589,
        "Y": -176.800676988458,
        "Z": -37.0764628583475,
        "ZoneSelectionList": ["main.1"],
    }
)
session.workflow.TaskObject["Identify Regions"].Arguments.setState(
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
session.workflow.TaskObject["Identify Regions"].AddChildToTask()

session.workflow.TaskObject["Identify Regions"].InsertCompoundChildTask()

session.workflow.TaskObject["fluid-region-1"].Arguments.setState(
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
session.workflow.TaskObject["Identify Regions"].Arguments.setState({})

session.workflow.TaskObject["fluid-region-1"].Execute()
session.workflow.TaskObject["Identify Regions"].Arguments.setState(
    {
        "MaterialPointsName": "void-region-1",
        "NewRegionType": "void",
        "ObjectSelectionList": ["inlet-1", "inlet-2", "inlet-3", "main"],
        "X": 374.722045740589,
        "Y": -278.9775145640143,
        "Z": -161.1700719416913,
    }
)
session.workflow.TaskObject["Identify Regions"].AddChildToTask()

session.workflow.TaskObject["Identify Regions"].InsertCompoundChildTask()

session.workflow.TaskObject["Identify Regions"].Arguments.setState({})

session.workflow.TaskObject["void-region-1"].Execute()

###############################################################################
# Define thresholds for any potential leakages.

session.workflow.TaskObject["Define Leakage Threshold"].Arguments.setState(
    {
        "AddChild": "yes",
        "FlipDirection": True,
        "PlaneDirection": "X",
        "RegionSelectionSingle": "void-region-1",
    }
)
session.workflow.TaskObject["Define Leakage Threshold"].AddChildToTask()

session.workflow.TaskObject["Define Leakage Threshold"].InsertCompoundChildTask()
session.workflow.TaskObject["leakage-1"].Arguments.setState(
    {
        "AddChild": "yes",
        "FlipDirection": True,
        "LeakageName": "leakage-1",
        "PlaneDirection": "X",
        "RegionSelectionSingle": "void-region-1",
    }
)
session.workflow.TaskObject["Define Leakage Threshold"].Arguments.setState(
    {
        "AddChild": "yes",
    }
)
session.workflow.TaskObject["leakage-1"].Execute()

###############################################################################
# Review your region settings.

session.workflow.TaskObject["Update Region Settings"].Arguments.setState(
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
session.workflow.TaskObject["Update Region Settings"].Execute()


###############################################################################
# Select options for controlling the mesh.

session.workflow.TaskObject["Choose Mesh Control Options"].Execute()

###############################################################################
# Generate the surface mesh.

session.workflow.TaskObject["Generate the Surface Mesh"].Execute()

###############################################################################
# Confirm and update the boundaries.

session.workflow.TaskObject["Update Boundaries"].Execute()

###############################################################################
# Add boundary layers.

session.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()

session.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()

session.workflow.TaskObject["aspect-ratio_1"].Arguments.setState(
    {
        "BLControlName": "aspect-ratio_1",
    }
)
session.workflow.TaskObject["Add Boundary Layers"].Arguments.setState({})

session.workflow.TaskObject["aspect-ratio_1"].Execute()

###############################################################################
# Generate the volume mesh.

session.workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
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
session.workflow.TaskObject["Generate the Volume Mesh"].Execute()

###############################################################################
# Check the mesh.

session.tui.meshing.mesh.check_mesh()

###############################################################################
# Switch to Solution mode.

session.tui.meshing.switch_to_solution_mode("yes")

session.tui.solver.mesh.check()

###############################################################################
# Set the units for length

session.tui.solver.define.units("length", "mm")

###############################################################################
# Select kw sst turbulence model

session.tui.solver.define.models.viscous.kw_sst("yes")

###############################################################################
# Set the velocity and turbulence boundary conditions for the first inlet
# (inlet-1).

session.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet-1", [], "vmag", "no", 1, "quit"
)

###############################################################################
# Apply the same conditions for the other velocity inlet boundaries (inlet_2,
# and inlet_3).

session.tui.solver.define.boundary_conditions.copy_bc(
    "inlet-1", "inlet-2", "inlet-3", ()
)

###############################################################################
# Set the boundary conditions at the outlet (outlet-1).

session.tui.solver.define.boundary_conditions.set.pressure_outlet(
    "outlet-1", [], "turb-intensity", 5, "quit"
)
session.tui.solver.solve.monitors.residual.plot("yes")

###############################################################################
# Initialize the flow field using the Initialization

session.tui.solver.solve.initialize.hyb_initialization()

###############################################################################
# Start the calculation by requesting 100 iterations

session.tui.solver.solve.set.number_of_iterations(100)
session.tui.solver.solve.iterate()

# session.tui.solver.report.volume_integrals.volume("fluid-region-1","()","yes","volume.vrp")

###############################################################################
# Display path lines highlighting the flow field

session.tui.solver.display.objects.create(
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
# session.tui.solver.display.objects.display("pathlines-1")

###############################################################################
# Create an iso-surface through the manifold geometry.

session.tui.solver.surface.iso_surface(
    "x-coordinate",
    "surf-x-coordinate",
    "()",
    "fluid-region-1",
    "()",
    "380",
    "()",
)

###############################################################################
# Create and define contours of velocity magnitude throughout the manifold
# along with the mesh.

session.tui.solver.display.objects.create(
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
# session.tui.solver.display.objects.display("contour-velocity")

session.tui.solver.display.objects.create(
    "mesh", "mesh-1", "surfaces-list", "*", "()", "quit"
)

###############################################################################
# Create a scene containing the mesh and the contours.

session.tui.solver.display.objects.create(
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
# session.tui.solver.display.objects.display("scene-1")

###############################################################################
# Save case, data and exit.
# session.tui.solver.file.write_case_data("exhaust_system.cas.h5")

# session.exit()
